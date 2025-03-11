import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Manually specify ChromeDriver path
chrome_driver_path = "C:\\New folder\\chromedriver-win64\\chromedriver.exe"

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Uncomment this after debugging
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open Flipkart FAQ page
driver.get("https://seller.flipkart.com/faq")
time.sleep(5)  # Wait for page to load

# Extract FAQs
faqs = []
faq_elements = driver.find_elements(By.XPATH, "//h3[contains(@class, 'styles__H3TextWrapper')]")

for index, faq in enumerate(faq_elements):
    try:
        question_text = faq.text.strip()
        
        # Click the question to expand the answer
        driver.execute_script("arguments[0].click();", faq)
        time.sleep(2)  # Allow time for answer to appear
        
        # Locate the answer relative to the clicked question
        answer_element = driver.find_element(By.XPATH, f"(//div[@class='rc-collapse-content-box'])[{index + 1}]")
        answer_text = answer_element.text.strip() if answer_element.text.strip() else "No answer found"

        faqs.append({"Question": question_text, "Answer": answer_text})
    
    except Exception as e:
        print(f"Error extracting FAQ {index + 1}: {str(e)}")

# Save FAQs to CSV
if faqs:
    df_faqs = pd.DataFrame(faqs)
    df_faqs.to_csv(r'E:\GUVI\faqs\flipkart_faqs.csv', index=False, encoding='utf-8')
    print("✅ FAQs saved to 'flipkart_faqs.csv'")
else:
    print("❌ No FAQs found.")

# Close WebDriver
driver.quit()
print("🎉 Script executed successfully!")


import pandas as pd

# Load the scraped FAQ dataset
df = pd.read_csv(r'E:\GUVI\faqs\flipkart_faqs.csv')

# Remove duplicates and empty answers
df = df.drop_duplicates().dropna().reset_index(drop=True)

# Save cleaned data
df.to_csv(r'E:\GUVI\faqs\flipkart_faqs_cleaned.csv', index=False, encoding='utf-8')

print("✅ Data cleaned and ready!")
