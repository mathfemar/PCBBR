from sqlmodel import Session
from sqlalchemy import text
from backend.database import engine
from backend.models import Build, BuildItem, Product
from datetime import datetime
from typing import List, Dict

def create_build(name: str) -> int:
    """Creates a new build and returns its ID"""
    with Session(engine) as session:
        query = text("""
            INSERT INTO build (name, created_at, updated_at)
            VALUES (:name, :created_at, :updated_at)
        """)
        session.execute(query, {
            "name": name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        session.commit()
        
        # Get the created build ID
        result = session.execute(text("SELECT last_insert_rowid()"))
        build_id = result.fetchone()[0]
        return build_id

def get_build(build_id: int) -> Dict:
    """Gets a build with all its items"""
    with Session(engine) as session:
        # Get build info
        build_query = text("SELECT * FROM build WHERE id = :build_id")
        build_result = session.execute(build_query, {"build_id": build_id})
        build_row = build_result.fetchone()
        
        if not build_row:
            return None
        
        # Get build items with product details
        items_query = text("""
            SELECT bi.id, bi.category, bi.added_at,
                   p.id, p.url, p.store, p.name, p.current_price, p.category, p.image_url
            FROM builditem bi
            JOIN product p ON bi.product_id = p.id
            WHERE bi.build_id = :build_id
            ORDER BY bi.category
        """)
        items_result = session.execute(items_query, {"build_id": build_id})
        items_rows = items_result.fetchall()
        
        items = []
        total_price = 0
        for row in items_rows:
            item = {
                "id": row[0],
                "category": row[1],
                "added_at": row[2],
                "product": {
                    "id": row[3],
                    "url": row[4],
                    "store": row[5],
                    "name": row[6],
                    "current_price": row[7],
                    "category": row[8],
                    "image_url": row[9]
                }
            }
            items.append(item)
            total_price += row[7]
        
        return {
            "id": build_row[0],
            "name": build_row[1],
            "created_at": build_row[2],
            "updated_at": build_row[3],
            "items": items,
            "total_price": total_price
        }

def add_item_to_build(build_id: int, product_id: int, category: str):
    """Adds a product to a build"""
    with Session(engine) as session:
        # Remove existing item in same category (if any)
        delete_query = text("""
            DELETE FROM builditem 
            WHERE build_id = :build_id AND category = :category
        """)
        session.execute(delete_query, {"build_id": build_id, "category": category})
        
        # Add new item
        insert_query = text("""
            INSERT INTO builditem (build_id, product_id, category, added_at)
            VALUES (:build_id, :product_id, :category, :added_at)
        """)
        session.execute(insert_query, {
            "build_id": build_id,
            "product_id": product_id,
            "category": category,
            "added_at": datetime.utcnow()
        })
        
        # Update build timestamp
        update_query = text("""
            UPDATE build SET updated_at = :updated_at WHERE id = :build_id
        """)
        session.execute(update_query, {
            "updated_at": datetime.utcnow(),
            "build_id": build_id
        })
        
        session.commit()

def remove_item_from_build(build_id: int, category: str):
    """Removes an item from a build by category"""
    with Session(engine) as session:
        query = text("""
            DELETE FROM builditem 
            WHERE build_id = :build_id AND category = :category
        """)
        session.execute(query, {"build_id": build_id, "category": category})
        session.commit()

def list_builds() -> List[Dict]:
    """Lists all builds"""
    with Session(engine) as session:
        query = text("""
            SELECT b.id, b.name, b.created_at, b.updated_at,
                   COUNT(bi.id) as item_count,
                   COALESCE(SUM(p.current_price), 0) as total_price
            FROM build b
            LEFT JOIN builditem bi ON b.id = bi.build_id
            LEFT JOIN product p ON bi.product_id = p.id
            GROUP BY b.id
            ORDER BY b.updated_at DESC
        """)
        result = session.execute(query)
        rows = result.fetchall()
        
        builds = []
        for row in rows:
            builds.append({
                "id": row[0],
                "name": row[1],
                "created_at": row[2],
                "updated_at": row[3],
                "item_count": row[4],
                "total_price": row[5]
            })
        
        return builds
