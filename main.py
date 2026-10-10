# ============================================================
# 豆包自动答题助手 - Android 打包版（Kivy）
# 适配安卓媒体投影捕获屏幕，一次授权持续读取屏幕，保留原有UI框架
# ============================================================
from kivy.core.text import LabelBase
# 思源黑体字体，把 NotoSansCJK-Regular.ttf 和 main.py 放同一目录
LabelBase.register(
    name="msyh",
    fn_regular="NotoSansCJK-Regular.otf"
)

import threading
import hashlib
import time
import requests
import base64
from io import BytesIO

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock

# ====================== 【请修改这里】百度OCR密钥 ======================
BAIDU_API_KEY = "bbtA5lXSvbdY3fW31UEn1fdJ"
BAIDU_SECRET_KEY = "08GHJQiHVy4NaIid4RHBthCXtfRnODDE"
# ======================================================================

# ============================================================
# ⚠️ 豆包 API Key
# ============================================================
DOUBAO_API_KEY        = "ark-9ff9c272-7bf7-45be-89ac-95f8b465db79-b584a"
DOUBAO_MODEL_ENDPOINT = "doubao-pro-32k-241215"
DOUBAO_API_URL        = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

# 获取百度token
def get_baidu_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_API_KEY}&client_secret={BAIDU_SECRET_KEY}"
    resp = requests.post(url)
    return resp.json()["access_token"]


class DoubaoQuizApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = False
        self.last_hash = ""
        self.last_answer_t = 0
        self.interval = 3.0
        self.token = get_baidu_token()
        self.capture_session = None
        self.android = None
        # 安卓环境导入屏幕捕获模块
        try:
            import android
            from android import media_projection
            self.android = android
            self.media_projection = media_projection
        except Exception:
            self.android = None

    def build(self):
        Window.title = "豆包答题助手"
        root = BoxLayout(orientation="vertical", padding=15, spacing=10)
        root.add_widget(Label(
            text="[b]📸 豆包自动答题[/b]\n点启动监听 → 授权屏幕捕获，自动识别屏幕题目",
            markup=True, size_hint_y=None, height=80, font_name="msyh"
        ))
        # API Key 输入（可选，怕硬编码泄露就加这个）
        self.api_input = TextInput(
            hint_text="豆包API Key（可选，不填用代码里的）",
            size_hint_y=None, height=40, font_name="msyh"
        )
        root.add_widget(self.api_input)

        # 监听开关
        self.btn = ToggleButton(
            text="▶ 启动监听",
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1,1,1,1), font_size=20, size_hint_y=None, height=70, font_name="msyh"
        )
        self.btn.bind(on_release=self.toggle)
        root.add_widget(self.btn)

        self.status = Label(text="状态：已停止", size_hint_y=None, height=35, color=(0.5,0.5,0.5,1), font_name="msyh")
        root.add_widget(self.status)

        self.preview = Label(text="(识别到的题目会显示在这里)",
                             size_hint=(1,1), text_size=(380, None), halign="left",
                             valign="top", color=(0.4,0.4,0.4,1), font_size=12, font_name="msyh")
        root.add_widget(self.preview)
        return root

    def toggle(self, btn):
        if btn.state == "down":
            if self.android is None:
                self.status.text = "错误：仅安卓打包后支持屏幕捕获！PC无法捕获屏幕"
                btn.state = "normal"
                return
            # 请求屏幕捕获授权（安卓系统弹窗，必须手动点允许）
            try:
                self.capture_session = self.media_projection.MediaProjection()
                self.capture_session.start()
            except Exception as e:
                self.status.text = f"屏幕捕获授权失败：{e}"
                btn.state = "normal"
                return

            # 取 API Key（优先用输入框）
            self.api_key = self.api_input.text.strip() or DOUBAO_API_KEY
            self.running = True
            btn.text = "■ 停止监听"
            btn.background_color = (0.9, 0.3, 0.3, 1)
            self.status.text = f"状态：监听中（每{self.interval}s读取屏幕）"
            self.status.color = (0.2,0.7,0.3,1)
            Clock.schedule_interval(self.loop, self.interval)
        else:
            self.running = False
            btn.text = "▶ 启动监听"
            btn.background_color = (0.2, 0.7, 0.3, 1)
            self.status.text = "状态：已停止"
            self.status.color = (0.5,0.5,0.5,1)
            Clock.unschedule(self.loop)
            if self.capture_session:
                self.capture_session.stop()
                self.capture_session = None

    def loop(self, dt):
        if not self.running or not self.capture_session:
            return
        try:
            # 获取屏幕截图帧
            frame = self.capture_session.capture_frame()
            buf = BytesIO()
            frame.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode()
        except Exception as e:
            self.status.text = f"读取屏幕失败:{e}"
            return

        # 百度在线OCR识别
        try:
            ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={self.token}"
            res = requests.post(ocr_url, data={"image": img_base64})
            words_list = [item["words"] for item in res.json().get("words_result", [])]
            text = "\n".join(words_list).strip()
        except Exception as e:
            self.status.text = f"OCR失败: {e}"
            return

        if len(text) < 4:
            return
        self.preview.text = text[:400]
        # 去重
        h = hashlib.md5(text.encode()).hexdigest()
        if h == self.last_hash and time.time()-self.last_answer_t < 5:
            return
        self.last_hash = h
        self.status.text = "🤖 询问豆包..."
        threading.Thread(target=self.call_doubao, args=(text,), daemon=True).start()

    def call_doubao(self, question):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": DOUBAO_MODEL_ENDPOINT,
            "messages": [
                {"role":"system","content":"快速答题：识别题目，按【答案】xxx【解析】一句话 简洁回答"},
                {"role":"user","content":question[:2000]}
            ],
            "temperature":0.2
        }
        try:
            resp = requests.post(DOUBAO_API_URL, headers=headers, json=payload, timeout=25)
            data = resp.json()
            if resp.status_code==200 and "choices" in data:
                ans = data["choices"][0]["message"]["content"]
                self.last_answer_t = time.time()
                Clock.schedule_once(lambda dt: self.popup(ans))
            else:
                Clock.schedule_once(lambda dt: self.popup(f"API错误：{data.get('error',{}).get('message','')}"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.popup(f"网络错误：{e}"))

    def popup(self, ans):
        box = BoxLayout(orientation="vertical", padding=15, spacing=10)
        box.add_widget(Label(text=ans, size_hint_y=None, height=300, text_size=(380,None),
                             halign="left", valign="top", font_size=14, color=(0.1,0.1,0.1,1), font_name="msyh"))
        btn = Button(text="知道了✓", size_hint_y=None, height=50, background_color=(0.2,0.7,0.3,1), color=(1,1,1,1), font_name="msyh")
        pop = Popup(title="🤖 豆包答案", content=box, size_hint=(0.92,0.55), auto_dismiss=False, separator_color=(0.2,0.7,0.3,1))
        btn.bind(on_press=pop.dismiss)
        box.add_widget(btn)
        pop.open()
        self.status.text = "✅ 答案已弹出"

if __name__ == "__main__":
    DoubaoQuizApp().run()
