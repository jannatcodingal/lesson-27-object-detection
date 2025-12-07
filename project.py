import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY
def generate_inpainting_imaage(prompt, image_path, mask_path):
    API_URL="https;//api-inference.huggingface.co/models/stailityai/stable-diffusion-inpainting"
    headers={"Authorization": f"Bearer {HF_API_KEY}"}
    with open(image_path, "rb") as img_file:
        image_data=img_file.read()
    with open(mask_path, "rb") as mask_file:
        mask_data=mask_file.read()
    payload={"inputs": prompt}
    files={
        "image": ("image.png", image_data,"image/png"),
        "mask":("mask.png", mask_data, "image/png")
    }
    response=requests.post(API_URL, headers=headers, data=payload, files=files)
    if response.status_code==200:
        inpainted_image=Image.open(BytesIO(response.content))
        return inpainted_image
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
def main():
    print("welcome to the Inpainting and restoration challenge!")
    print("This activity allows you to restore or transform parts of an existing image.")
    print("Provide a base image, a mask indicating the areas to modify, and a text prompt describing the desired changes.")
    print("Type 'exit' to quit the program.")
    while True:
        prompt=input("Enter a description for the inpainting (or 'exit' to quit):\n")
        if prompt.lower()=="exit":
            print("Exiting the program. Goodbye!")
            break
        image_path=input("Enter the path to the base image:\n")
        if image_path.lower()=='exit':
            break
        mask_path=input("Enter the path to the mask image:\n")
        if mask_path.lower()=='exit':
            break
        try:
            print("\nProcessing inpainting...")
            result_image=generate_inpainting_imaage(prompt, image_path, mask_path)
            result_image.show()
            save_path=input("Enter the path to save the inpainted image (yes/no): ").strip().lower()
            if save_path=='yes':
                output_path=input("Enter the output file path without extension: ").strip()
                result_image.save(f"{output_path}.png")
                print(f"Inpainted image saved to {output_path}.png")
            print("-"*80+"\n")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.\n")
if __name__=="__main__":
    main()