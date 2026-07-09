import streamlit as st
import requests
from streamlit_geolocation import streamlit_geolocation

# 1. Cấu hình trang
st.set_page_config(page_title="Bếp Mẹ Bom", page_icon="🍱", layout="wide")

# Custom CSS cho icon nổi và thiết kế
st.markdown("""
<style>
/* CSS cho Icon nổi ở góc dưới */
.floating-zalo { position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px; z-index: 9999; cursor: pointer; transition: transform 0.2s;}
.floating-mess { position: fixed; bottom: 90px; right: 20px; width: 60px; height: 60px; z-index: 9999; cursor: pointer; transition: transform 0.2s;}
.floating-zalo:hover, .floating-mess:hover { transform: scale(1.1); }

/* Chỉnh ảnh bo góc và cố định tỷ lệ */
img[data-testid="stImage"] {
    border-radius: 12px;
    object-fit: cover;
    aspect-ratio: 1 / 1;
}

/* Loại bỏ padding thừa của container */
[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
</style>
<a href="https://zalo.me/0886873388" target="_blank">
    <img class="floating-zalo" src="https://upload.wikimedia.org/wikipedia/commons/9/91/Icon_of_Zalo.svg" alt="Zalo"/>
</a>
<a href="https://m.me/theubinh16062014" target="_blank">
    <img class="floating-mess" src="https://upload.wikimedia.org/wikipedia/commons/b/be/Facebook_Messenger_logo_2020.svg" alt="Messenger"/>
</a>
""", unsafe_allow_html=True)

# 2. Cấu hình Telegram Bot (Thay thế bằng Token và Chat ID thật)
TELEGRAM_BOT_TOKEN = "8685247292:AAEsGy0S2JT0ek0yQyiDesp3rTTQeCKv6mQ"
TELEGRAM_CHAT_ID = "763228783"

# 3. Khởi tạo giỏ hàng trong Session State
if "cart" not in st.session_state:
    st.session_state.cart = {}

def add_to_cart(name, option, price):
    item_key = f"{name}_{option}"
    if item_key in st.session_state.cart:
        st.session_state.cart[item_key]['quantity'] += 1
    else:
        st.session_state.cart[item_key] = {
            "name": name,
            "option": option,
            "price": price,
            "quantity": 1
        }
    st.toast(f"Đã thêm {name} vào giỏ hàng! 🛒", icon="✅")

# 4. Data Menu (Đã thêm img và desc)
# Tạm thời dùng ảnh minh họa từ Unsplash
IMG_BANH_BAO = "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?q=80&w=300&auto=format&fit=crop"
IMG_MON_MAN = "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?q=80&w=300&auto=format&fit=crop"
IMG_AN_NHE = "https://images.unsplash.com/photo-1562967914-608f82629710?q=80&w=300&auto=format&fit=crop"
IMG_CANH = "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=300&auto=format&fit=crop"

MENU = {
    "Bánh bao Handmade": [
        {"name": "Thịt Trứng", "price": 60000, "unit": "4c", "items_per_pack": 4, "img": IMG_BANH_BAO, "desc": "Bánh bao nhân thịt trứng cút đậm đà truyền thống"},
        {"name": "Xá Xíu Phô Mai", "price": 75000, "unit": "4c", "items_per_pack": 4, "img": IMG_BANH_BAO, "desc": "Bánh nhân xá xíu đậm vị kết hợp phô mai béo ngậy"},
        {"name": "Bò Ngô Phô Mai", "price": 75000, "unit": "4c", "items_per_pack": 4, "img": IMG_BANH_BAO, "desc": "Bò băm xào ngô ngọt và phô mai kéo sợi cực hấp dẫn"},
        {"name": "Xúc Xích Phô Mai", "price": 75000, "unit": "4c", "items_per_pack": 4, "img": IMG_BANH_BAO, "desc": "Xúc xích Đức cao cấp hòa quyện phô mai"},
        {"name": "Gạo Lứt Gà Nấm PM", "price": 75000, "unit": "4c", "items_per_pack": 4, "img": IMG_BANH_BAO, "desc": "Vỏ gạo lứt tốt cho sức khỏe nhân ức gà nấm hương (Eat clean)"},
        {"name": "Lá Dứa Nhân Đậu", "price": 40000, "unit": "4c", "items_per_pack": 4, "img": IMG_BANH_BAO, "desc": "Bánh bao ngọt thơm mùi lá dứa tự nhiên nhân đậu xanh"},
        {"name": "Bánh Bao Chay", "price": 35000, "unit": "5c", "items_per_pack": 5, "img": IMG_BANH_BAO, "desc": "Bánh chay không nhân thanh đạm, dẻo thơm"},
    ],
    "Món mặn đưa cơm": [
        {"name": "Thịt Kho Tàu", "price": 95000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Thịt ba chỉ chuẩn rọi kho trứng cút mềm rục béo ngậy"},
        {"name": "Sườn Sốt Chua Ngọt", "price": 105000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Sườn non hảo hạng chiên xù xém cạnh sốt chua ngọt"},
        {"name": "Lòng Xào Dưa", "price": 50000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Lòng non xào dưa chua giòn sần sật, đưa cơm cực kỳ"},
        {"name": "Mực Xào Cần Tỏi", "price": 110000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Mực nang tươi xào cần tỏi thơm lừng hấp dẫn"},
        {"name": "Chả Lá Lốt", "price": 75000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Chả thịt băm cuộn lá lốt chiên vàng, thơm phưng phức"},
        {"name": "Chả Viên Nướng", "price": 85000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Chả viên nướng chảo tẩm ướp gia vị gia truyền"},
        {"name": "Cá Trắm Mix Kho Dưa", "price": 95000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Cá trắm đen kho dưa chua tốn cơm vô cùng"},
        {"name": "Cá Trắm Mix Kho Chuối", "price": 95000, "unit": "Suất", "img": IMG_MON_MAN, "desc": "Cá trắm đen kho chuối xanh thịt ba chỉ truyền thống"},
    ],
    "Ăn nhẹ & ăn vặt": [
        {"name": "Cơm Nắm", "price": 30000, "unit": "Suất", "img": IMG_AN_NHE, "desc": "Cơm nắm muối vừng/ruốc dẻo thơm gợi nhớ tuổi thơ"},
        {"name": "Kimbap", "price": 35000, "unit": "Suất", "img": IMG_AN_NHE, "desc": "Cơm cuộn rong biển chuẩn vị Hàn, nhân đầy đặn"},
        {"name": "Bánh Gà - Đã chiên sơ", "price": 60000, "unit": "10c", "img": IMG_AN_NHE, "desc": "Bánh ức gà rau củ tẩm bột chiên sơ tiện lợi"},
        {"name": "Bánh chả lá chanh", "price": 170000, "unit": "Kg", "img": IMG_AN_NHE, "desc": "Bánh chả nướng thơm lừng mùi lá chanh, mỡ phần giòn sần sật"},
        {"name": "Nem Thịt Truyền Thống", "price": 90000, "unit": "11c", "img": IMG_AN_NHE, "desc": "Nem rán nhân thịt truyền thống (gói sẵn đã chiên sơ)"},
        {"name": "Pate Đặc Biệt (400g)", "price": 65000, "unit": "Hộp", "img": IMG_AN_NHE, "desc": "Pate gan heo đặc biệt thơm béo ngậy đóng hộp 400g"},
        {"name": "Pate Đặc Biệt (500g)", "price": 80000, "unit": "Hộp", "img": IMG_AN_NHE, "desc": "Pate gan heo đặc biệt thơm béo ngậy đóng hộp 500g"},
    ],
    "Các món canh": [
        {"name": "Canh Cà Bung Đậu Thịt", "price": 60000, "unit": "Bát", "img": IMG_CANH, "desc": "Canh cà tím bung thịt ba chỉ rán cháy cạnh thơm mùi tía tô"},
        {"name": "Canh Sườn Nấu Dưa", "price": 60000, "unit": "Bát", "img": IMG_CANH, "desc": "Canh sườn non nấu dưa chua giải ngấy ngày hè"},
        {"name": "Ốc Om Chuối Đậu", "price": 75000, "unit": "Bát", "img": IMG_CANH, "desc": "Ốc nhồi làm sạch om chuối đậu thịt ba chỉ đậm đà"},
    ]
}

# 5. UI Layout - Header
st.title("🍱 HOMEMADE FOOD & CATERING")
st.markdown("### BẾP MẸ BOM")
st.markdown("Khám phá hương vị cơm nhà ấm cúng, chuẩn vị gia đình Việt.")
st.divider()

# Hiển thị các block tags (như anchor links) ở trên cùng để khách bấm vào
tags_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;'>"
for idx, cat in enumerate(MENU.keys()):
    tags_html += f"<a href='#menu-section-{idx}' target='_self' style='text-decoration: none;'><span style='background-color: #e8f5e9; color: #2e7d32; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px; border: 1px solid #c8e6c9; display: inline-block; transition: all 0.2s;'>{cat}</span></a>"
tags_html += "</div>"
st.markdown(tags_html, unsafe_allow_html=True)

# Hiển thị Menu theo chiều dọc toàn bộ
for idx, (cat_name, items) in enumerate(MENU.items()):
    # Đặt thẻ div ẩn làm điểm neo (anchor). top: -60px giúp khi nhảy không bị che khuất bởi header
    st.markdown(f"<div id='menu-section-{idx}' style='position: relative; top: -60px;'></div>", unsafe_allow_html=True)
    st.markdown(f"#### 🍲 {cat_name}")
    
    # Tạo lưới 2 cột
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        
        # Hàm render từng món
        def render_item(item, col):
            with col:
                # Container đóng khung món ăn (giống Card)
                with st.container(border=True):
                    c_img, c_info = st.columns([1.5, 3])
                    
                    with c_img:
                        st.image(item['img'], use_container_width=True)
                        
                    with c_info:
                        st.markdown(f"**{item['name']}**")
                        st.markdown(f"<span style='color:#757575; font-size:13px;'>{item['desc']}</span>", unsafe_allow_html=True)
                        
                        # Cột cho Giá và Nút để xếp thẳng hàng ngang
                        cp1, cp2 = st.columns([1.2, 1])
                        with cp1:
                            st.markdown(f"<div style='margin-top:12px;'><strong><span style='color:#d84315; font-size: 16px;'>{item['price']:,}đ</span></strong> <span style='font-size:12px'>/ {item['unit']}</span></div>", unsafe_allow_html=True)
                        
                        with cp2:
                            # Xử lý nút bấm theo Category (Riêng bánh bao có tùy chọn)
                            if cat_name == "Bánh bao Handmade":
                                opt = st.radio("Loại", ["Theo hộp", "Theo cái"], key=f"rad_{item['name']}", horizontal=True, label_visibility="collapsed")
                                price = item['price'] if opt == "Theo hộp" else int(item['price'] / item['items_per_pack'])
                                if st.button("🛒 Đặt", key=f"btn_{item['name']}_{opt}", type="primary", use_container_width=True):
                                    add_to_cart(item['name'], opt, price)
                            else:
                                if st.button("🛒 Đặt", key=f"btn_{item['name']}", type="primary", use_container_width=True):
                                    add_to_cart(item['name'], "Mặc định", item['price'])
        
        # Render cột 1
        if i < len(items):
            render_item(items[i], cols[0])
        # Render cột 2
        if i + 1 < len(items):
            render_item(items[i+1], cols[1])
            
    st.divider() # Vạch ngăn cách giữa các danh mục

# --- CỘT TRÁI (SIDEBAR): Giỏ hàng và Form Checkout ---
with st.sidebar:
    st.header("🛒 Giỏ Hàng Của Bạn")
    
    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Hãy thêm món ăn vào giỏ nhé!")
    else:
        total_amount = 0
        for key, item in list(st.session_state.cart.items()):
            item_total = item['price'] * item['quantity']
            total_amount += item_total
            
            with st.container(border=True):
                st.markdown(f"**{item['name']}**")
                if item['option'] != "Mặc định":
                    st.markdown(f"<span style='font-size:12px; color:gray'>({item['option']})</span>", unsafe_allow_html=True)
                
                c_qty, c_price = st.columns([1, 1])
                new_qty = c_qty.number_input("SL", min_value=0, value=item['quantity'], key=f"qty_{key}", label_visibility="collapsed")
                c_price.markdown(f"<div style='text-align:right; margin-top:8px'>**{item_total:,}đ**</div>", unsafe_allow_html=True)
                
                if new_qty == 0:
                    del st.session_state.cart[key]
                    st.rerun()
                elif new_qty != item['quantity']:
                    st.session_state.cart[key]['quantity'] = new_qty
                    st.rerun()
            
        st.markdown("---")
        st.markdown(f"### Tổng cộng: <span style='color:#d84315'>{total_amount:,}đ</span>", unsafe_allow_html=True)
        
        st.subheader("Thông tin nhận hàng")
        st.markdown("**📍 Tự động lấy vị trí (Khuyên dùng)**", help="Bấm vào đây để cấp quyền lấy vị trí chính xác của bạn giúp Shipper giao hàng dễ hơn.")
        loc = streamlit_geolocation()
        google_maps_link = ""
        if loc and loc.get('latitude') and loc.get('longitude'):
            google_maps_link = f"https://www.google.com/maps?q={loc['latitude']},{loc['longitude']}"
            st.success("Đã nhận được tọa độ vị trí của bạn!")
            
        with st.form("checkout_form"):
            name = st.text_input("Tên người đặt (*)", placeholder="Nhập họ tên")
            phone = st.text_input("Số điện thoại (*)", placeholder="Nhập SĐT")
            address = text_area_val = st.text_area("Địa chỉ giao hàng (*)", placeholder="Nếu đã chia sẻ vị trí ở trên, chỉ cần nhập thêm Số nhà/ngõ")
            
            submitted = st.form_submit_button("🚀 Gửi Đơn Hàng", type="primary", use_container_width=True)
            
            if submitted:
                if not name.strip() or not phone.strip() or not address.strip():
                    st.error("⚠️ Vui lòng nhập đầy đủ Tên, SĐT và Địa chỉ.")
                else:
                    order_lines = []
                    for k, v in st.session_state.cart.items():
                        opt_str = "" if v['option'] == "Mặc định" else f" ({v['option']})"
                        order_lines.append(f"- {v['name']}{opt_str} x {v['quantity']} = {v['price']*v['quantity']:,}đ")
                        
                    order_text = (
                        f"🔔 **ĐƠN HÀNG MỚI - BẾP MẸ BOM** 🔔\n\n"
                        f"👤 Khách hàng: {name}\n"
                        f"📞 SĐT: {phone}\n"
                        f"🏠 Địa chỉ: {address}\n"
                    )
                    
                    if google_maps_link:
                        order_text += f"📍 **Tọa độ Map:** {google_maps_link}\n"
                        
                    order_text += (
                        f"\n📦 **Chi tiết món:**\n"
                        + "\n".join(order_lines) +
                        f"\n\n💰 **TỔNG CỘNG: {total_amount:,}đ**"
                    )
                    
                    try:
                        # Gửi tin nhắn tự động qua Telegram API
                        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                        payload = {
                            "chat_id": TELEGRAM_CHAT_ID,
                            "text": order_text.replace('**', '*')  # Làm gọn text cho dễ nhìn trên Telegram
                        }
                        
                        resp = requests.post(url, json=payload)
                        
                        if resp.status_code == 200:
                            st.session_state.cart = {}
                            st.success("✅ Đặt hàng thành công! Đơn hàng đã được tự động thông báo tới quán.")
                            st.balloons()
                        else:
                            st.error(f"❌ Đơn hàng chưa gửi được. Vui lòng kiểm tra lại cấu hình Telegram Bot. Lỗi: {resp.text}")
                    except Exception as e:
                        st.error(f"❌ Có lỗi mạng khi kết nối tới Telegram: {e}")
