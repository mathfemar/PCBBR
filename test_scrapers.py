import fetch_terabyte
import fetch_pichau

def run_tests():
    print("--- PCBBR Scraper Tests ---\n")
    
    # 1. TerabyteShop
    print("Testing TerabyteShop...")
    tera_url = "https://www.terabyteshop.com.br/produto/30040/processador-amd-ryzen-5-9600x-39ghz-54ghz-turbo-6-cores-12-threads-am5-sem-cooler-100-100001405wof"
    try:
        result = fetch_terabyte.fetch_product(tera_url)
        print(f"Result: {result}")
        if result.get('price'):
            print("✅ Terabyte Success")
        else:
            print("❌ Terabyte Failed")
    except Exception as e:
        print(f"❌ Terabyte Crash: {e}")

    print("\n---------------------------\n")

    # 2. Pichau
    print("Testing Pichau...")
    pichau_url = "https://www.pichau.com.br/placa-de-video-palit-geforce-rtx-5060-ti-infinity-3-16gb-gddr7-128-bit-ne7506t019t1-gb2061s"
    try:
        result = fetch_pichau.fetch_product(pichau_url)
        print(f"Result: {result}")
        if result.get('price'):
            print("✅ Pichau Success")
        else:
            print("❌ Pichau Failed")
    except Exception as e:
        print(f"❌ Pichau Crash: {e}")

    print("\n---------------------------\n")

    # 3. Kabum
    print("Testing Kabum...")
    kabum_url = "https://www.kabum.com.br/produto/609956/processador-amd-ryzen-5-9600x-3-9-ghz-5-4-ghz-cache-32-mb-6-nucleos-12-threads-am5-100-100001405wof"
    try:
        import fetch_kabum
        result = fetch_kabum.fetch_product(kabum_url)
        print(f"Result: {result}")
        if result.get('price'):
            print("✅ Kabum Success")
        else:
            print("❌ Kabum Failed")
    except Exception as e:
        print(f"❌ Kabum Crash: {e}")

    print("\n---------------------------\n")

    # 4. Amazon
    print("Testing Amazon...")
    amazon_url = "https://www.amazon.com.br/Processador-AMD-Ryzen-5-5600G/dp/B092L9GF5N/"
    try:
        import fetch_amazon
        result = fetch_amazon.fetch_product(amazon_url)
        print(f"Result: {result}")
        if result.get('price'):
            print("✅ Amazon Success")
        else:
            print("❌ Amazon Failed")
    except Exception as e:
        print(f"❌ Amazon Crash: {e}")
        
    print("\n---------------------------")

if __name__ == "__main__":
    run_tests()
