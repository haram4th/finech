from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
from io import StringIO
import time
from ex_dbio import to_ex_db

def new_col(df):
    new_cols = []
    for col in df.columns:
        if col[0] == col[1] == col[2]:
            new_cols.append(col[0].strip().replace(" ", "_"))
        else:
            new_cols.append(" ".join(col).strip().replace(" ", "_"))
    return new_cols

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("start-maximized")
options.add_argument("Chrome/135.0.0.0")
options.add_argument("lang=ko_KR")
# 웹브라우저가 백그라운드에서 작동하도록 설정
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
    )

url = "https://www.kebhana.com/cms/rate/index.do?contentUrl=/cms/rate/wpfxd651_01i.do"
driver.get(url)

wait = WebDriverWait(driver, 20)

# 오늘날짜 20250411 형식으로 가져오기
today = datetime.datetime.now()
date = f"{today.year}-{today.month:02d}-{today.day:02d}"

date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tmpInqStrDt")))
date_input.clear()
date_input.send_keys(date.replace("-", ""))
date_input.send_keys(Keys.ENTER)

# 조회버튼 클릭
search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#HANA_CONTENTS_DIV > div.btnBoxCenter > a")))
search_button.click()
time.sleep(2)
df = pd.read_html(StringIO(driver.find_element(By.CSS_SELECTOR, ".tblBasic.leftNone").get_attribute('outerHTML')))[0]
df['date'] = date
new_columns = new_col(df)
df.columns = new_columns
df = df[['date', '통화', '현찰_사실_때_환율', '현찰_사실_때_Spread', '현찰_파실_때_환율', '현찰_파실_때_Spread',
   '송금_보낼_때_보낼_때', '송금_받을_때_받을_때', '외화_수표_파실때', '매매_기준율', '환가_료율',
   '미화_환산율']]
to_ex_db(df)
print(f"{date} 환율정보 DB 저장 완료", end="\r")
