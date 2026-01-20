CATEGORIES = [
    'CPU',
    'CPU Cooler',
    'Motherboard',
    'Memory',
    'SSD',
    'Hard Drive',
    'Video Card',
    'Case',
    'Power Supply',
    'Monitor'
]

# Mapeamento de categorias para URLs de busca de cada loja
CATEGORY_URLS = {
    'kabum': {
        'CPU': 'https://www.kabum.com.br/hardware/processadores',
        'Video Card': 'https://www.kabum.com.br/hardware/placa-de-video-vga',
        'Motherboard': 'https://www.kabum.com.br/hardware/placas-mae',
        'Memory': 'https://www.kabum.com.br/hardware/memoria-ram',
        'Hard Drive': 'https://www.kabum.com.br/hardware/disco-rigido-hd',
        'SSD': 'https://www.kabum.com.br/hardware/ssd-2-5',
        'CPU Cooler': ['https://www.kabum.com.br/hardware/coolers/air-cooler', 
                        'https://www.kabum.com.br/hardware/coolers/water-cooler'],
        'Power Supply': 'https://www.kabum.com.br/hardware/fontes',
        'Case': 'https://www.kabum.com.br/hardware/gabinetes',
        'Monitor': 'https://www.kabum.com.br/computadores/monitores/monitor-gamer'
    },
    'pichau': {
        'CPU': 'https://www.pichau.com.br/hardware/processadores',
        'Video Card': 'https://www.pichau.com.br/hardware/placa-de-video',
        'Motherboard': 'https://www.pichau.com.br/hardware/placa-m-e',
        'Memory': 'https://www.pichau.com.br/hardware/memorias',
        'SSD': 'https://www.pichau.com.br/hardware/ssd-m-2',
        'Hard Drive': 'https://www.pichau.com.br/hardware/hard-disk-e-ssd',
        'CPU Cooler': 'https://www.pichau.com.br/hardware/cooler-processador',
        'Power Supply': 'https://www.pichau.com.br/hardware/fonte',
        'Case': 'https://www.pichau.com.br/hardware/gabinete',
        'Monitor': 'https://www.pichau.com.br/monitores/monitores-gamer'
    },
    'terabyte': {
        'CPU': 'https://www.terabyteshop.com.br/processadores',
        'Video Card': 'https://www.terabyteshop.com.br/placa-de-video',
        'Motherboard': 'https://www.terabyteshop.com.br/placa-mae',
        'Memory': 'https://www.terabyteshop.com.br/memorias',
        'Hard Drive': 'https://www.terabyteshop.com.br/hard-disk/ha-sata-iii',
        'SSD': 'https://www.terabyteshop.com.br/hard-disk/ssd',
        'CPU Cooler': 'https://www.terabyteshop.com.br/refrigeracao/cooler-p-cpu',
        'Power Supply': 'https://www.terabyteshop.com.br/fontes',
        'Case': 'https://www.terabyteshop.com.br/gabinetes',
        'Monitor': 'https://www.terabyteshop.com.br/monitor'
    }
}
