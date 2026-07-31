import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.extensions import db
from backend.models.collection import CollectionModel
from backend.models.collection_banner import CollectionBanner

def test_api():
    print("[TEST] Running Collection Banners API verification test...")
    with app.test_client() as client:
        # 1. Fetch collection
        with app.app_context():
            coll = CollectionModel.query.first()
            if not coll:
                coll = CollectionModel(name="Wedding Wear", slug="wedding-wear", description="Bridal collection")
                db.session.add(coll)
                db.session.commit()
            coll_id = coll.id
            coll_name = coll.name

        print(f"[TEST] Using collection ID {coll_id}: '{coll_name}'")

        # 2. Test GET dynamic banner before creation (should return banner: null)
        res_get_empty = client.get(f'/api/collection-banners/{coll_name}')
        print("GET empty banner response status:", res_get_empty.status_code, res_get_empty.json)

        # 3. Create test CollectionBanner directly in DB for testing GET
        with app.app_context():
            existing = CollectionBanner.query.filter_by(collection_id=coll_id).first()
            if not existing:
                cb = CollectionBanner(
                    collection_id=coll_id,
                    banner_image="/luxury_solitaire_ring.png",
                    title="The Royal Kundan Bridal Collection",
                    subtitle="WEDDING WEAR",
                    description="Discover handcrafted bridal sets made in premium gold.",
                    button_text="SHOP WEDDING WEAR",
                    button_link="/?collection=Wedding%20Wear",
                    is_active=True,
                    display_order=1
                )
                db.session.add(cb)
                db.session.commit()
                print("[TEST] Inserted test CollectionBanner in DB.")

        # 4. Test GET dynamic banner after creation
        res_get = client.get(f'/api/collection-banners/{coll_name}')
        print("GET collection banner status:", res_get.status_code)
        banner_data = res_get.json.get("banner")
        print("GET banner data:", banner_data)

        assert res_get.status_code == 200
        assert banner_data is not None
        assert banner_data.get("collection_id") == coll_id
        assert banner_data.get("banner_image") == "/luxury_solitaire_ring.png"
        assert banner_data.get("title") == "The Royal Kundan Bridal Collection"
        assert banner_data.get("status") == "Active"

        # 5. Test GET all collection banners
        res_all = client.get('/api/collection-banners')
        print("GET all collection banners count:", len(res_all.json))
        assert res_all.status_code == 200
        assert len(res_all.json) >= 1

        print("✅ ALL BACKEND COLLECTION BANNER API TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_api()
