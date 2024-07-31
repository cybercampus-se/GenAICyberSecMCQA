from openai import OpenAI



client = OpenAI(
    base_url="http://localhost:8086/v1",
    api_key="token-abc123",
)

# completion = client.chat.completions.create(
#   model="microsoft/Phi-3-vision-128k-instruct",
#   messages=[
#     {"role": "user", "content": "Hello!"}
  
#   ]
# )
# print(completion.choices[0].message)

import base64

# Path to the image file
image_path = "/home/sb7059/git/GenAICyberSecMCQA/data/Images_350_701/Q_4.png"

# Open the image file in binary mode
with open(image_path, "rb") as image_file:
    # Read the binary data of the image file
    image_binary = image_file.read()
    
    # Encode the binary data to base64
    image_base64 = base64.b64encode(image_binary).decode('utf-8')

response = client.chat.completions.create(
  model="microsoft/Phi-3-vision-128k-instruct",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}",
          }, 
        },
      ],
    }
  ],
  max_tokens=300,
)
print(response.choices[0])
