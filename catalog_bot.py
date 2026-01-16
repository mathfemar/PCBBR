"""
Catalog Bot - Automated Product Cataloging

This script runs the catalog update process to scrape product listings
from all stores and categories. It should be run daily via Task Scheduler
or cron to keep the product catalog up to date.

Usage:
    python catalog_bot.py              # Update all categories
    python catalog_bot.py --category CPU  # Update specific category
    python catalog_bot.py --store kabum   # Update specific store
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from services import catalog_service

# Configure logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"catalog_bot_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main bot execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Product Catalog Bot")
    parser.add_argument("--category", help="Update specific category only")
    parser.add_argument("--store", help="Update specific store only")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Starting Catalog Bot")
    logger.info("=" * 60)
    
    try:
        if args.category:
            logger.info(f"Updating category: {args.category}")
            count = catalog_service.catalog_products_by_category(
                args.category, 
                args.store
            )
            logger.info(f"[OK] Cataloged {count} products for {args.category}")
        else:
            logger.info("Updating all categories...")
            count = catalog_service.catalog_all_products()
            logger.info(f"[OK] Total products cataloged: {count}")
        
        logger.info("=" * 60)
        logger.info("Catalog Bot finished successfully")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"✗ Error running catalog bot: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
