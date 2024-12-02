import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init

init(autoreset=True)

save_directory = "downloaded_files"
os.makedirs(save_directory, exist_ok=True)

def get_asset_name(asset_id):
    url = f"https://assetdelivery.roblox.com/v1/asset/?ID={asset_id}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('name', f'asset_{asset_id}') 
        else:
            print(f"{Fore.RED}Failed to get asset name for {asset_id}, status code: {response.status_code}")
            return f'asset_{asset_id}' 
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching asset name for {asset_id}: {e}")
        return f'asset_{asset_id}'  


def download_asset(i):
    url = f"https://assetdelivery.roblox.com/v1/asset/?ID={i}"
    
    asset_name = get_asset_name(i)
    
    try:
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            safe_asset_name = asset_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
            
            file_path = os.path.join(save_directory, f"{safe_asset_name}_{i}.rbxl")
            
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"{Fore.GREEN}Successfully saved file: {file_path}")
        else:
            print(f"{Fore.RED}Failed request for {url}, status code: {response.status_code}")
    
    except requests.exceptions.Timeout as e:
        print(f"{Fore.YELLOW}Timeout error requesting {url}: {e}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error requesting {url}: {e}")


def main():

    num_threads = 300  
    

    with ThreadPoolExecutor(max_workers=num_threads) as executor:

        futures = [executor.submit(download_asset, i) for i in range(999999, 9999999999)] 
        
 
        for future in as_completed(futures):
            future.result() 

    print(f"{Fore.GREEN}Download completed!")

if __name__ == "__main__":
    main()