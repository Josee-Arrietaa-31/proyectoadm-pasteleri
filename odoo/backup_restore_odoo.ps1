param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("export", "import")]
    [string]$Mode,

    [Parameter(Mandatory = $true)]
    [string]$DbName,

    [string]$BackupDir = ".\\respaldo_odoo",
    [string]$ProjectDir = ".",
    [string]$DbService = "db",
    [string]$WebService = "web",
    [string]$DbUser = "odoo",
    [string]$DumpPath = "",
    [string]$FilestoreTarPath = "",
    [switch]$FixedName
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Compose {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    Push-Location $ProjectDir
    try {
        & docker compose @Args
    }
    finally {
        Pop-Location
    }
}

function Ensure-Dir {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Ensure-ParentDir {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$defaultDumpWithTimestamp = Join-Path $BackupDir ("{0}_{1}.dump" -f $DbName, $timestamp)
$defaultFilestoreDirWithTimestamp = Join-Path $BackupDir ("filestore_{0}_{1}" -f $DbName, $timestamp)
$defaultDumpFixed = Join-Path $BackupDir ("{0}.dump" -f $DbName)
$defaultFilestoreFixed = Join-Path $BackupDir ("filestore_{0}.tar" -f $DbName)

if ($Mode -eq "export") {
    Ensure-Dir -Path $BackupDir

    if ($DumpPath) {
        $dumpFile = $DumpPath
    }
    elseif ($FixedName) {
        $dumpFile = $defaultDumpFixed
    }
    else {
        $dumpFile = $defaultDumpWithTimestamp
    }

    if ($FilestoreTarPath) {
        $filestoreTarFile = $FilestoreTarPath
    }
    elseif ($FixedName) {
        $filestoreTarFile = $defaultFilestoreFixed
    }
    else {
        Ensure-Dir -Path $defaultFilestoreDirWithTimestamp
        $filestoreTarFile = Join-Path $defaultFilestoreDirWithTimestamp "filestore_$DbName.tar"
    }

    Ensure-ParentDir -Path $dumpFile
    Ensure-ParentDir -Path $filestoreTarFile

    Write-Host "[1/3] Exportando base de datos '$DbName'..."
    Invoke-Compose -Args @(
        "exec", "-T", $DbService,
        "bash", "-lc",
        "pg_dump -U $DbUser -Fc $DbName > /tmp/$DbName.dump"
    )

    Write-Host "[2/3] Copiando dump a '$dumpFile'..."
    Invoke-Compose -Args @("cp", "$DbService`:/tmp/$DbName.dump", $dumpFile)

    Write-Host "[3/3] Exportando filestore..."
    # Odoo 17 suele usar /var/lib/odoo/filestore/<db>; algunos despliegues usan .local/share/Odoo/filestore/<db>
    Invoke-Compose -Args @(
        "exec", "-T", $WebService,
        "bash", "-lc",
        "if [ -d /var/lib/odoo/filestore/$DbName ]; then tar -C /var/lib/odoo/filestore -cf /tmp/filestore_$DbName.tar $DbName; elif [ -d /var/lib/odoo/.local/share/Odoo/filestore/$DbName ]; then tar -C /var/lib/odoo/.local/share/Odoo/filestore -cf /tmp/filestore_$DbName.tar $DbName; else echo 'Filestore no encontrado para la base' && exit 1; fi"
    )
    Invoke-Compose -Args @("cp", "$WebService`:/tmp/filestore_$DbName.tar", $filestoreTarFile)

    Write-Host "Respaldo listo:"
    Write-Host "- Dump: $dumpFile"
    Write-Host "- Filestore: $filestoreTarFile"
    exit 0
}

if ($Mode -eq "import") {
    if ($DumpPath) {
        if (-not (Test-Path -LiteralPath $DumpPath)) {
            throw "No se encontro dump en '$DumpPath'."
        }
        $importDumpPath = $DumpPath
    }
    elseif ($FixedName) {
        if (-not (Test-Path -LiteralPath $defaultDumpFixed)) {
            throw "No se encontro dump fijo en '$defaultDumpFixed'."
        }
        $importDumpPath = $defaultDumpFixed
    }
    else {
        $latestDump = Get-ChildItem -LiteralPath $BackupDir -Filter "$DbName*.dump" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if (-not $latestDump) {
            throw "No se encontro dump para '$DbName' en '$BackupDir'."
        }
        $importDumpPath = $latestDump.FullName
    }

    if ($FilestoreTarPath) {
        if (-not (Test-Path -LiteralPath $FilestoreTarPath)) {
            throw "No se encontro filestore en '$FilestoreTarPath'."
        }
        $importFilestorePath = $FilestoreTarPath
    }
    elseif ($FixedName) {
        if (-not (Test-Path -LiteralPath $defaultFilestoreFixed)) {
            throw "No se encontro filestore fijo en '$defaultFilestoreFixed'."
        }
        $importFilestorePath = $defaultFilestoreFixed
    }
    else {
        $latestTar = Get-ChildItem -LiteralPath $BackupDir -Recurse -Filter "filestore_$DbName.tar" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if (-not $latestTar) {
            throw "No se encontro filestore_$DbName.tar en '$BackupDir'."
        }
        $importFilestorePath = $latestTar.FullName
    }

    Write-Host "[1/5] Copiando dump al contenedor..."
    Invoke-Compose -Args @("cp", $importDumpPath, "$DbService`:/tmp/$DbName.dump")

    Write-Host "[2/5] Recreando base de datos '$DbName'..."
    Invoke-Compose -Args @(
        "exec", "-T", $DbService,
        "bash", "-lc",
        "dropdb -U $DbUser --if-exists $DbName; createdb -U $DbUser $DbName"
    )

    Write-Host "[3/5] Restaurando dump..."
    Invoke-Compose -Args @(
        "exec", "-T", $DbService,
        "bash", "-lc",
        "pg_restore -U $DbUser -d $DbName --clean --if-exists /tmp/$DbName.dump"
    )

    Write-Host "[4/5] Restaurando filestore..."
    Invoke-Compose -Args @("cp", $importFilestorePath, "$WebService`:/tmp/filestore_$DbName.tar")
    Invoke-Compose -Args @(
        "exec", "-T", $WebService,
        "bash", "-lc",
        "mkdir -p /var/lib/odoo/filestore; tar -C /var/lib/odoo/filestore -xf /tmp/filestore_$DbName.tar || (mkdir -p /var/lib/odoo/.local/share/Odoo/filestore; tar -C /var/lib/odoo/.local/share/Odoo/filestore -xf /tmp/filestore_$DbName.tar)"
    )

    Write-Host "[5/5] Reiniciando servicios..."
    Invoke-Compose -Args @("restart")

    Write-Host "Importacion completada para '$DbName'."
    exit 0
}