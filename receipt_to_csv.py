import easyocr

reader = easyocr.Reader(['en'])  # specify the language
result = reader.readtext('./IMG_5004.jpeg')

for (bbox, text, prob) in result:
    print(f'Text: {text}, Probability: {prob}')
