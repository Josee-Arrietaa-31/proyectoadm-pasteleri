{
    'name': 'Pan & Aroma - Tema Personalizado',
    'version': '17.0.1.0.0',
    'category': 'Theme',
    'author': 'Pan & Aroma',
    'website': 'https://panyaroma.com',
    'license': 'AGPL-3',
    'depends': ['web', 'website'],
    'data': [
        'static/description/index.html',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_theme/static/src/css/theme.css',
        ],
        'web.assets_frontend': [
            'custom_theme/static/src/css/website_theme.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': ['static/description/icon.png'],
}
