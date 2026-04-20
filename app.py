import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import io
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Siamraj Sales Dashboard v3.0", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Arimo:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');
    
    /* 🔥 คืนค่าฟอนต์ระบบให้ Streamlit แบบเบาบาง ไม่ใช้ * เพื่อป้องกันไอคอนลูกศรพัง */
    html, body, p, h1, h2, h3, h4, h5, h6, table, th, td, input, select, textarea, .stMarkdown {
        font-family: 'Canva Sans', 'Sarabun', sans-serif;
    }

    /* 🔥 บังคับให้ส่วนที่เป็นไอคอนกลับมาใช้ Material Symbols ของ Streamlit อย่างถูกต้อง */
    .material-symbols-rounded, 
    .material-symbols-outlined, 
    .material-icons,
    span[class*="material-symbols"], 
    [data-testid="stSidebarCollapseButton"] *, 
    button[kind="header"] *, 
    [data-testid="collapsedControl"] * {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* 🔥 ลดพื้นที่ว่างด้านบนสุดของหน้า Dashboard แบบสุดๆ */
    [data-testid="stAppViewBlockContainer"] { padding-top: 0rem !important; padding-bottom: 1rem !important; }
    .reportview-container .main .block-container { padding-top: 0rem !important; }
    .css-1d391kg { padding-top: 0rem !important; }
    
    /* แก้ไข: เปลี่ยนจาก display: none เป็นพื้นหลังโปร่งใส เพื่อให้ปุ่มลูกศรซ่อน/แสดง Sidebar กลับมาทำงานได้ปกติ */
    header[data-testid="stHeader"] { background-color: transparent !important; } 

    h1, h2, h3, h4, h5, h6 { color: #2B3467; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        white-space: pre-wrap;
        background-color: #e2e8f0;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: #475569;
        font-weight: 700;
        font-size: 15px;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #cbd5e1;
        color: #1e293b;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #2B3467 !important; 
        color: white !important; 
        border-bottom: 4px solid #ef4444 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .metric-card {
        background-color: white; border: 1px solid #e0e0e0; padding: 20px;
        border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); text-align: center;
    }
    .metric-value { font-size: 28px; font-weight: bold; color: #2B3467; }
    .metric-target { font-size: 14px; color: #7f8c8d; }
    .metric-profit { font-size: 18px; font-weight: bold; color: #e74c3c; }
    
    .custom-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; background-color: white; }
    .custom-table th, .custom-table td { padding: 4px 8px; border-bottom: 1px solid #f1f5f9; }
    .custom-table thead th { background-color: #f8fafc; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 10px; border-bottom: 2px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; }
    .custom-table .group-row { background-color: #f1f5f9; font-weight: bold; color: #334155; }
    .custom-table .text-right { text-align: right; }
    .custom-table .text-center { text-align: center; }
    
    /* ========================================== */
    /* 🔥 CUSTOM GRID BUTTONS FOR SIDEBAR FILTERS */
    /* ========================================== */
    
    /* 1. ลดพื้นที่ว่างด้านบนสุดของ Sidebar */
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem !important;
    }

    /* 2. ปรับแต่งปุ่มกด Sidebar ให้อยู่ในรูปแบบ Grid (Pill Buttons) */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 10px;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        flex: 1 1 calc(22% - 6px); /* โชว์แถวละประมาณ 4 กล่อง */
        min-width: 44px;
        justify-content: center;
        align-items: center;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        border-radius: 6px !important;
        padding: 4px 2px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important; /* ป้องกันคำตกบรรทัด */
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #f1f5f9 !important;
        border-color: #94a3b8 !important;
    }
    
    /* 🔥 3. แสดงสีพื้นหลังเมื่อถูกเลือก (Sidebar Active State) */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] {
        background-color: #4f46e5 !important;
        border-color: #4f46e5 !important;
        box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2) !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) span,
    [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] p {
        color: white !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > label p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label span {
        color: #475569 !important;
        font-size: 11.5px !important;
        margin: 0 !important;
        text-align: center !important;
        white-space: nowrap !important; /* ป้องกันคำตกบรรทัด */
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-of-type {
        display: none !important; /* ซ่อนวงกลมปุ่ม Radio เดิมทิ้ง */
    }
    
    /* ========================================== */
    /* 🔥 MAIN CONTENT RADIO BUTTONS (Plan Sales / Plan Account) */
    /* ========================================== */
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* บังคับไม่ให้ตัดคำขึ้นบรรทัดใหม่ */
        gap: 8px !important;
    }
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label {
        flex: 1 1 50% !important; /* ขนาด 50/50 เท่ากันเป๊ะ */
        max-width: 50% !important;
        justify-content: center !important;
        align-items: center !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label:hover {
        background-color: #f1f5f9 !important;
        border-color: #94a3b8 !important;
    }
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label:has(input:checked),
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[aria-checked="true"] {
        background-color: #4f46e5 !important;
        border-color: #4f46e5 !important;
        box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2) !important;
    }
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label:has(input:checked) p,
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[data-checked="true"] p,
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[aria-checked="true"] p {
        color: white !important;
        font-weight: 700 !important;
    }
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label p {
        color: #475569 !important;
        font-size: 14px !important;
        margin: 0 !important;
        text-align: center !important;
        white-space: nowrap !important; /* บังคับข้อความไม่ให้ตกบรรทัด */
    }
    [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label > div:first-of-type {
        display: none !important; /* ซ่อนวงกลมปุ่ม Radio เดิมทิ้ง */
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ส่วนหัว HTML พื้นฐาน และ JS Modal สำหรับ AI ฉบับยิงตรง (Direct API Call - Instant Failover)
# ==========================================
COMMON_HTML_HEAD = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
    * { font-family: 'Canva Sans', 'Sarabun', sans-serif !important; }
    body { margin: 0; padding: 0; background-color: white; overflow-x: hidden; }
    .custom-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 12px; background-color: white; }
    .custom-table th, .custom-table td { padding: 4px 8px; border-bottom: 1px solid #f1f5f9; }
    .custom-table thead th { background-color: #f8fafc; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 10px; border-bottom: 2px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; }
    .custom-table .group-row { background-color: #f1f5f9; font-weight: bold; color: #334155; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { background: #c7c7cc; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #a1a1aa; }
    .rotate-icon { display: inline-block; transition: transform 0.2s; }
    
    /* AI Modal CSS */
    .modal-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:9999; align-items:center; justify-content:center; backdrop-filter: blur(4px); }
    .modal-content { background:white; width:95%; max-width:900px; height:85vh; border-radius:12px; display:flex; flex-direction:column; box-shadow: 0 10px 25px rgba(0,0,0,0.2); animation: fadeIn 0.3s ease; overflow: hidden; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    
    /* AI Content Formatting */
    #aiModalBody { padding: 24px; overflow-y: auto; flex: 1; font-size: 13.5px; color: #374151; line-height: 1.7; }
    #aiModalBody h3 { font-size: 16px; font-weight: 700; margin-top: 24px; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 2px solid #e5e7eb; }
    #aiModalBody h3:nth-of-type(1) { color: #b45309; border-color: #fef3c7; }
    #aiModalBody h3:nth-of-type(2) { color: #1d4ed8; border-color: #eff6ff; }
    #aiModalBody h3:nth-of-type(3) { color: #047857; border-color: #ecfdf5; }
    #aiModalBody h3:nth-of-type(4) { color: #be123c; border-color: #fff1f2; }
    #aiModalBody ul { padding-left: 24px; margin-bottom: 16px; }
    #aiModalBody li { margin-bottom: 6px; }
    #aiModalBody strong { color: #111827; }
    
    .action-plan-box { background-color: #f3f4f6; padding: 16px 20px; border-radius: 8px; border-left: 4px solid #6366f1; margin-top: 12px; font-size: 13px; }
    .step-text { color: #4f46e5; font-weight: bold; }
</style>
<script>
    function toggleGroup(cls, btn) {
        var elms = document.getElementsByClassName(cls);
        if (elms.length === 0) return;
        var willShow = (elms[0].style.display === 'none' || elms[0].style.display === '');
        for(var i=0; i<elms.length; i++) { elms[i].style.display = willShow ? 'table-row' : 'none'; }
        var arrow = btn.querySelector('.arrow-icon');
        if (arrow) { arrow.innerHTML = willShow ? '▲' : '▼'; }
    }
    
    function toggleDetail(id, btn) {
        var r = document.getElementById(id);
        if (!r) return;
        var willShow = (r.style.display === 'none' || r.style.display === '');
        r.style.display = willShow ? 'table-row' : 'none';
        var icon = btn.querySelector('.rotate-icon');
        if (icon) { icon.style.transform = willShow ? 'rotate(180deg)' : 'rotate(0deg)'; }
    }
    
    let currentAiArgs = {};

    function saveLocalKeyAndRun() {
        const val = document.getElementById('tempApiKey').value.trim();
        if(val) {
            localStorage.setItem('local_gemini_key', val);
            triggerAI(currentAiArgs.custName, currentAiArgs.ind, currentAiArgs.lastProd, currentAiArgs.lastDate);
        } else {
            alert('กรุณาใส่ API Key ก่อนบันทึก');
        }
    }

    function resetLocalKey() {
        localStorage.removeItem('local_gemini_key');
        alert('ล้าง API Key ในเครื่องสำเร็จแล้ว');
        document.getElementById('aiModal').style.display='none';
    }
    
    function showKeyInputScreen(body, errorDetails = "") {
        let errorHtml = "";
        if (errorDetails) {
            errorHtml = `<div style="background-color:#fef2f2; color:#b91c1c; padding:12px; border-radius:6px; border:1px solid #fecaca; margin-bottom:16px; font-size:12px; text-align:left;"><b>⚠️ พบปัญหาจาก Key เดิม:</b><br>${errorDetails}</div>`;
        }
        
        body.innerHTML = `
            <div style="text-align:center; padding:30px 20px; max-width: 500px; margin: 0 auto;">
                <i class="fa-solid fa-key" style="font-size:48px; color:#f59e0b; margin-bottom:16px;"></i>
                <h3 style="color:#b45309; margin-bottom:12px; border:none; justify-content:center;">จำเป็นต้องใช้ API Key ของ Google AI Studio</h3>
                ${errorHtml}
                <div style="text-align:left; background-color:#f3f4f6; padding:16px; border-radius:8px; margin-bottom:20px; font-size:13px; color:#374151;">
                    <b>วิธีรับ API Key ฟรี (1 นาที):</b>
                    <ol style="margin-top:8px; padding-left:20px; line-height:1.6;">
                        <li>คลิกลิงก์ 👉 <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#3b82f6; font-weight:bold; text-decoration:none;">Google AI Studio</a></li>
                        <li>กดปุ่มสีฟ้า <b>"Create API key"</b></li>
                        <li>เลือก <b>"Create API key in new project"</b></li>
                        <li>Copy รหัสที่ได้มาวางในช่องด้านล่างนี้</li>
                    </ol>
                </div>
                <input type="password" id="tempApiKey" placeholder="วาง API Key (ขึ้นต้นด้วย AIzaSy...)" style="width:100%; padding:12px 14px; border:2px solid #d1d5db; border-radius:8px; margin-bottom:20px; font-size:14px; font-family:monospace; text-align:center; transition: border-color 0.3s;" onfocus="this.style.borderColor='#4f46e5'" onblur="this.style.borderColor='#d1d5db'">
                <br>
                <button onclick="saveLocalKeyAndRun()" style="background:#4f46e5; color:white; padding:12px 24px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; font-size:14px; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><i class="fa-solid fa-bolt" style="margin-right:8px;"></i> บันทึก & วิเคราะห์ข้อมูลเลย</button>
            </div>
        `;
    }
    
    async function triggerAI(custName, ind, lastProd, lastDate) {
        currentAiArgs = { custName, ind, lastProd, lastDate };
        let activeKey = localStorage.getItem('local_gemini_key') || "";
        
        const modal = document.getElementById('aiModal');
        const body = document.getElementById('aiModalBody');
        modal.style.display = 'flex';
        
        // 1. ตรวจสอบ API Key ก่อน
        if (!activeKey) {
            showKeyInputScreen(body);
            return;
        }
        
        // 2. แสดงหน้าจอ Loading
        body.innerHTML = `
            <div style="text-align:center; padding:80px 20px;">
                <i class="fa-solid fa-circle-notch fa-spin" style="font-size:50px; color:#4f46e5; margin-bottom:24px;"></i>
                <h3 style="color:#4f46e5; margin:0; font-size:18px; border:none; justify-content:center;">กำลังเจาะลึกข้อมูลบัญชี: <span style="color:#111827; margin-left:8px;">${custName}</span></h3>
                <p style="color:#6b7280; font-size:14px; margin-top:16px;">
                    <i class="fa-solid fa-microchip" style="margin-right: 8px; color:#3b82f6;"></i>กำลังวิเคราะห์สิทธิ์ API และสแกนหาโมเดลที่ดีที่สุด...<br>
                    <span style="font-size:12px; color:#9ca3af;">(กระบวนการนี้จะการันตีว่าจะไม่เกิด Model Not Found)</span>
                </p>
            </div>
        `;

        const fullPrompt = `คุณคือ "Senior B2B Sales Strategist & Industrial Analyst" ของบริษัท สยามราช บมจ.
หน้าที่ของคุณคือวิเคราะห์ข้อมูลลูกค้าเพื่อให้ฝ่ายขายนำไปวาง Action Plan

ข้อมูลผลิตภัณฑ์ของสยามราช (เพื่ออ้างอิง):
- WF, VK: VIKING (Gear & Hygienic Pump)
- WR: SANDPIPER (AODD)
- CG: COGNITO (EODD)
- CK: CORKEN (COMPRESSOR)
- LC: LC METER (PD Meter)
- GP, GL: GOULDS PUMPS & WATER
- KB: KSB PUMP & VALVE
- TN: POMPETRAVAINI
- IM: IMO (Multi screw)
- SP: SEEPEX (Single screw)
- HV: HOWDEN TURBO
- SE: SES & KWANGSHIN
- VP: PIGGING SYSTEM

ข้อมูลลูกค้าที่ต้องวิเคราะห์:
- ชื่อบริษัท: "${custName}"
- อุตสาหกรรม: ${ind}
- ประวัติการซื้อล่าสุดกับสยามราช: ซื้อ ${lastProd} เมื่อ ${lastDate}

ข้อกำหนดการตอบ: ตอบกลับด้วยการจัดรูปแบบ Markdown ตามโครงสร้างด้านล่างนี้ "เท่านั้น" ห้ามออกนอกโครงสร้างนี้

### 🏢 1. ข้อมูลนิติบุคคลและภาพรวมธุรกิจ (AI Estimated Profile)
- **ชื่อลูกค้า:** [ชื่อบริษัท]
- **อุตสาหกรรม:** [อุตสาหกรรม]
- **ประวัติล่าสุดกับสยามราช:** [ข้อมูลการซื้อล่าสุด]
- **ลักษณะธุรกิจ:** [ประเมินจากชื่อและอุตสาหกรรมว่าผลิตอะไรหรือให้บริการอะไร]

### ⚙️ 2. กระบวนการผลิตและของเหลวที่ใช้
- **กระบวนการผลิต:** [อธิบายกระบวนการผลิตคร่าวๆ ที่น่าจะเกิดขึ้นในโรงงานนี้]
- **สารเคมี/ของเหลวที่ใช้ (เน้นพิเศษ):** [ระบุชื่อสารเคมี ของเหลว หรือก๊าซ ที่โรงงานอุตสาหกรรมประเภทนี้ต้องใช้]
- **Pain Point ที่คาดการณ์:** [ปัญหาที่ลูกค้าน่าจะเจอเกี่ยวกับการสูบจ่ายของเหลวหรือสารเคมี]

### 💡 3. โอกาสในการต่อยอด (Cross-sell / Up-sell)
- **การใช้สินค้าเดิม:** [อธิบายว่าสินค้าเดิมที่ลูกค้าเคยซื้อ น่าจะถูกเอาไปใช้ทำอะไรในโรงงาน]
- **สินค้านำเสนอเพิ่มเติม:** [แนะนำแบรนด์/สินค้าอื่นของสยามราชที่เข้ากับโรงงานนี้ พร้อมบอกเหตุผล]

### 🎯 4. แผนปฏิบัติการ (Action Plan) สำหรับทีมขาย
<div class="action-plan-box">
<span class="step-text">Step 1 (เข้าถึง):</span> [คำแนะนำวิธีติดต่อลูกค้าเกริ่นนำ]<br><br>
<span class="step-text">Step 2 (นำเสนอ):</span> [คำแนะนำโซลูชันที่จะนำไปเสนอ]<br><br>
<span class="step-text">Step 3 (ปิดจบ):</span> [กลยุทธ์การกระตุ้นให้ตัดสินใจซื้อ]
</div>`;

        try {
            // =======================================================================
            // 💡 นวัตกรรม Auto-Discovery: เข้าไปดึงรายชื่อโมเดลจาก API Key ของคุณโดยตรง!
            // วิธีนี้จะทำให้เราทราบชื่อ Model ที่คุณมีสิทธิ์ใช้อย่างแท้จริง (แก้ปัญหา 404 เด็ดขาด)
            // =======================================================================
            const modelsCheckRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${activeKey}`);
            
            if (!modelsCheckRes.ok) {
                const errData = await modelsCheckRes.json();
                throw new Error("API_KEY_INVALID: " + (errData.error?.message || "Invalid API Key"));
            }
            
            const modelsData = await modelsCheckRes.json();
            
            // กรองหาโมเดลที่รองรับฟังก์ชันการ Generate Text
            const validModels = modelsData.models.filter(m => 
                m.supportedGenerationMethods && m.supportedGenerationMethods.includes("generateContent")
            );

            // เรียงลำดับความฉลาด (Priority) ให้เลือก Flash 1.5 ก่อน
            let bestModel = validModels.find(m => m.name.includes("gemini-1.5-flash"));
            if (!bestModel) bestModel = validModels.find(m => m.name.includes("gemini-1.5-pro"));
            if (!bestModel) bestModel = validModels.find(m => m.name.includes("gemini-1.0-pro"));
            if (!bestModel) bestModel = validModels.find(m => m.name.includes("gemini-pro"));
            if (!bestModel && validModels.length > 0) bestModel = validModels[0]; // ถ้าไม่เจอเลย เอาตัวแรกที่ใช้ได้

            if (!bestModel) {
                throw new Error("MODEL_NOT_FOUND: บัญชี Google AI Studio ของคุณยังไม่เปิดให้ใช้โมเดลสร้างข้อความใดๆ เลย");
            }

            // --- 2. เปลี่ยนหน้าจอเป็น "เริ่มประมวลผลด้วยโมเดลที่สแกนเจอ" ---
            body.innerHTML = `
                <div style="text-align:center; padding:80px 20px;">
                    <i class="fa-solid fa-circle-notch fa-spin" style="font-size:50px; color:#4f46e5; margin-bottom:24px;"></i>
                    <h3 style="color:#4f46e5; margin:0; font-size:18px; border:none; justify-content:center;">กำลังเจาะลึกข้อมูลบัญชี: <span style="color:#111827; margin-left:8px;">${custName}</span></h3>
                    <p style="color:#6b7280; font-size:14px; margin-top:16px;">
                        <i class="fa-solid fa-check-circle" style="margin-right: 8px; color:#10b981;"></i>เชื่อมต่อโมเดล <b>${bestModel.displayName || bestModel.name}</b> สำเร็จ!<br>
                        <span style="font-size:12px; color:#9ca3af;">(กำลังประมวลผล Action Plan...)</span>
                    </p>
                </div>
            `;

            // =======================================================================
            // 💡 เรียกใช้งาน AI ด้วย Model ที่สแกนเจอเมื่อสักครู่
            // =======================================================================
            const payload = {
                contents: [{ parts: [{ text: fullPrompt }] }]
            };
            
            const endpoint = `https://generativelanguage.googleapis.com/v1beta/${bestModel.name}:generateContent?key=${activeKey}`;

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error?.message || `HTTP ${response.status} Error`);
            }
            
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
            if(!text) throw new Error("API ประมวลผลสำเร็จ แต่ไม่ได้ส่งข้อความตอบกลับมา");
            
            // พิมพ์ผลลัพธ์ลงจอทันที
            body.innerHTML = marked.parse(text);
            
        } catch (err) {
            let errorMsg = err.message;
            let showResetBtn = false;
            
            if (errorMsg.includes("API_KEY_INVALID") || errorMsg.includes("API key not valid") || errorMsg.includes("400") || errorMsg.includes("unregistered callers")) {
                errorMsg = "API Key ของคุณไม่ถูกต้อง (Invalid API Key) กรุณาตรวจสอบว่า Copy มาครบทุกตัวอักษรหรือไม่";
                showResetBtn = true;
            } else if (errorMsg.includes("403") || errorMsg.includes("permission")) {
                errorMsg = "API Key ของคุณไม่มีสิทธิ์เข้าถึง (Permission Denied) หรือไม่ได้เปิดใช้งาน API ใน Google Cloud";
                showResetBtn = true;
            } else if (errorMsg.includes("429") || errorMsg.includes("quota")) {
                errorMsg = "โควต้าการใช้งาน AI ของคุณถูกใช้จนเต็ม (Quota Exceeded) กรุณารอสักครู่แล้วลองใหม่";
            }
            
            body.innerHTML = `
                <div style="text-align:center; padding:40px 20px; color:#b91c1c; background-color:#fef2f2; border-radius:8px;">
                    <i class="fa-solid fa-triangle-exclamation" style="font-size:50px; margin-bottom:16px; color:#ef4444;"></i>
                    <h3 style="border:none; color:#991b1b; justify-content:center; margin-bottom:8px;">พบข้อผิดพลาดจากฝั่ง Google AI</h3>
                    <p style="font-size:13px; margin-bottom:24px; color:#6b7280; font-family:monospace; word-wrap: break-word; background:white; padding:10px; border:1px solid #fecaca;">${errorMsg}</p>
                    <button onclick="resetLocalKey()" style="background:#ef4444; color:white; padding:8px 16px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; font-size:12px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);"><i class="fa-solid fa-rotate-right" style="margin-right:6px;"></i> ${showResetBtn ? 'ล้าง API Key แล้วตั้งค่าใหม่' : 'ล้าง API Key ในเครื่อง'}</button>
                </div>
            `;
        }
    }
</script>

<!-- AI Modal HTML Structure -->
<div id="aiModal" class="modal-overlay" onclick="if(event.target === this) this.style.display='none'">
    <div class="modal-content" onclick="event.stopPropagation()">
        <div style="padding:16px 24px; background: linear-gradient(135deg, #312e81 0%, #4f46e5 100%); color:white; border-radius:12px 12px 0 0; display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; font-size:16px; font-weight:bold; color:white; border:none; display:flex; align-items:center;"><i class="fa-solid fa-robot" style="margin-right:8px;"></i> Siamraj AI Account Analyzer</h3>
            <button onclick="document.getElementById('aiModal').style.display='none'" style="background:none; border:none; color:white; font-size:24px; cursor:pointer; padding:0; line-height:1;">&times;</button>
        </div>
        <div id="aiModalBody">
            <!-- AI Content goes here -->
        </div>
        <div style="padding:16px 24px; background:#f9fafb; border-top:1px solid #e5e7eb; border-radius:0 0 12px 12px; text-align:right;">
            <span style="float:left; font-size:11px; color:#9ca3af; margin-top:6px;"><i class="fa-solid fa-bolt" style="margin-right:4px;"></i>Powered by Gemini 1.5 Series (Auto-Discovery)</span>
            <button onclick="document.getElementById('aiModal').style.display='none'" style="background:#4f46e5; color:white; border:none; padding:8px 24px; border-radius:6px; font-size:13px; font-weight:bold; cursor:pointer; box-shadow:0 2px 4px rgba(0,0,0,0.1);">ปิดหน้าต่าง</button>
        </div>
    </div>
</div>
"""

# ==========================================
# 2. DATA PROCESSING HELPERS
# ==========================================
TH_MONTHS = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
TH_MONTHS_FULL = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]

def safe_fmt(v, decimals=0):
    try:
        if pd.isna(v): return "0"
        return f"{float(v):,.{decimals}f}"
    except:
        return "0"

def safe_pct(a, p):
    try:
        a = float(a) if pd.notna(a) else 0.0
        p = float(p) if pd.notna(p) else 0.0
        if p == 0: return "0%"
        return f"{(a/p*100):.0f}%"
    except:
        return "0%"

def format_th_date(dt):
    try:
        if pd.isna(dt) or dt.year < 1900: return "-"
        y = dt.year
        if y < 2400: y += 543
        y_short = y % 100
        m_idx = int(dt.month)
        if m_idx < 1 or m_idx > 12: return "-"
        return f"{TH_MONTHS[m_idx]} {y_short:02d}"
    except:
        return "-"

def format_exact_th_date(dt):
    try:
        if pd.isna(dt) or dt.year < 1900: return "-"
        y = dt.year
        if y < 2400: y += 543
        m_idx = int(dt.month)
        d = int(dt.day)
        if m_idx < 1 or m_idx > 12: return "-"
        return f"{d} {TH_MONTHS[m_idx]} {y}"
    except:
        return "-"

def clean_num(series):
    if series is None: return pd.Series([0.0])
    s = series.astype(str).str.replace(',', '', regex=False).str.strip()
    s = s.str.replace(r'^\((.*)\)$', r'-\1', regex=True)
    return pd.to_numeric(s, errors='coerce').fillna(0.0)

def get_col_data(df, keys, fallIdx=-1):
    cols = list(df.columns)
    cols_lower = [str(c).lower().strip() for c in cols]
    for k in keys:
        if k.lower().strip() in cols_lower: return df.iloc[:, cols_lower.index(k.lower().strip())]
    for k in keys:
        for i, c in enumerate(cols_lower):
            if k.lower().strip() in c: return df.iloc[:, i]
    if 0 <= fallIdx < len(cols): return df.iloc[:, fallIdx]
    return pd.Series(['']*len(df))

def get_col_by_index(df, idx, fill_val=''):
    if 0 <= idx < len(df.columns): return df.iloc[:, idx]
    return pd.Series([fill_val]*len(df))

def clean_cust(n):
    if pd.isna(n): return "Unknown"
    c = str(n)
    for f in ["บริษัท", "จำกัด", "มหาชน", "บจก.", "บมจ.", "หจก.", "Co., Ltd.", "Inc."]:
        c = re.sub(f, '', c, flags=re.IGNORECASE)
    return re.sub(r'\(\s*\)', '', c).strip()

def normalize_grp(g):
    if pd.isna(g): return 'Others'
    s = str(g).upper().strip()
    if 'COM' in s: return 'COM'
    if 'PD' in s: return 'PD'
    if any(x in s for x in [' A', 'A', 'กรุ๊ป A', 'GRP A']): return 'A'
    if any(x in s for x in [' B', 'B', 'กรุ๊ป B', 'GRP B']): return 'B'
    if any(x in s for x in [' C', 'C', 'กรุ๊ป C', 'GRP C']): return 'C'
    if any(x in s for x in [' D', 'D', 'กรุ๊ป D', 'GRP D']): return 'D'
    if any(x in s for x in [' R', 'R', 'กรุ๊ป R', 'GRP R']): return 'R'
    return 'Others'

def format_num_short(v):
    try:
        if pd.isna(v) or v == 0: return '-'
        v = float(v)
        if abs(v) >= 1e6: return f"{(v/1e6):.2f}"
        if abs(v) >= 1e3: return f"{(v/1e3):.1f}k"
        return f"{v:,.0f}"
    except:
        return "-"

def escape_html(text):
    if not isinstance(text, str): return str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def escape_js(text):
    if not isinstance(text, str): return str(text)
    return text.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')

# ==========================================
# 3. DATA FETCHING (AUTOMATED & PRE-COMPUTED)
# ==========================================
def get_gdrive_direct_url(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

@st.cache_data(ttl=3600)
def load_data():
    gdrive_files = {
        'plan': '1GAg_GW4KiswMGEq_TmUSGTiqZjZHRvKw',
        'so': '1OwmZ7tGlBV_saZoPUdNnusy-N1G4kqC5',
        'indiv_plan': '1zGIOI7l48zyu7YySnlLcCQgA6Di3Bx-2',
        'soi': '1M_7pEApQMSsgB6f9TelF933hxwBFoKTF',
        'inv_plan': '1G1NdO3y5ijTexplLSU8p0OMUFerFSYBF',
        'inv': '11NWmOJObDKjLEQ75DkRKZQ8t6II6OWj3'
    }
    
    data = {}
    try:
        with st.spinner('กำลังโหลดข้อมูลและปรับจูนประสิทธิภาพการทำงาน (Optimization)...'):
            # --- 1. โหลดไฟล์ PLAN ---
            df_raw_plan = pd.read_csv(get_gdrive_direct_url(gdrive_files['plan']))
            df_plan = pd.DataFrame({
                'Year': get_col_data(df_raw_plan, ['Data.Year', 'Year', 'year'], 5).astype(str).str.replace(r'\.0$', '', regex=True).str.strip(),
                'Month': pd.to_numeric(get_col_data(df_raw_plan, ['Data.Month', 'Month'], 6), errors='coerce').fillna(0),
                'Product': get_col_data(df_raw_plan, ['Data.ProductAdj', 'Product'], 8),
                'Group': get_col_data(df_raw_plan, ['Data.SalesGroupAdj', 'SalesGroup', 'Group'], 9).apply(normalize_grp),
                'Target': clean_num(get_col_data(df_raw_plan, ['Data.Value', 'Value'], 4))
            })
            df_plan = df_plan[(df_plan['Year'] != '') & (pd.to_numeric(df_plan['Year'], errors='coerce') > 2000)]
            data['plan_norm'] = df_plan
            
            # --- 2. โหลดไฟล์ SO ---
            df_raw_so = pd.read_csv(get_gdrive_direct_url(gdrive_files['so']), low_memory=False, header=0)
            
            try:
                parsed_so_dates = pd.to_datetime(df_raw_so.iloc[:, 2], errors='coerce')
                valid_so_dates = parsed_so_dates[parsed_so_dates <= pd.Timestamp.now() + pd.Timedelta(days=365)]
                data['latest_so'] = valid_so_dates.max() if not valid_so_dates.empty else pd.NaT
            except:
                data['latest_so'] = pd.NaT
            
            df_so = pd.DataFrame({
                'Year': get_col_by_index(df_raw_so, 28, '').astype(str).str.replace(r'\.0$', '', regex=True).str.strip(),
                'Month': pd.to_numeric(get_col_by_index(df_raw_so, 29, 0), errors='coerce').fillna(0),
                'Product': get_col_by_index(df_raw_so, 6, ''),
                'Group': get_col_by_index(df_raw_so, 16, '').apply(normalize_grp),
                'Actual': clean_num(get_col_by_index(df_raw_so, 20, 0)),
                'Margin': clean_num(get_col_by_index(df_raw_so, 22, 0)),
                'CustomerRaw': get_col_by_index(df_raw_so, 10, ''),
                'Industry': get_col_by_index(df_raw_so, 13, 'Unknown'),
                'SalesRep': get_col_by_index(df_raw_so, 15, 'Unknown'),
                'SONumber': get_col_by_index(df_raw_so, 4, '').astype(str).str.strip(),
                'RegYear': get_col_by_index(df_raw_so, 30, '').astype(str).str.replace(r'\.0$', '', regex=True).str.strip(),
                'RegMonth': pd.to_numeric(get_col_by_index(df_raw_so, 31, 0), errors='coerce').fillna(0),
                'QuotationNo': get_col_by_index(df_raw_so, 19, '').astype(str).str.strip()
            })
            df_so['Customer'] = df_so['CustomerRaw'].apply(clean_cust)
            df_so = df_so[(df_so['Year'] != '') & (pd.to_numeric(df_so['Year'], errors='coerce') > 2000)]
            
            df_so['SODate'] = pd.to_datetime(df_so['Year'].astype(str) + '-' + df_so['Month'].astype(int).astype(str).str.zfill(2) + '-01', errors='coerce')
            data['so_norm'] = df_so
            
            # --- 3. โหลดไฟล์ INDIVIDUAL PLAN ---
            df_raw_indiv = pd.read_csv(get_gdrive_direct_url(gdrive_files['indiv_plan']), header=0)
            df_indiv = pd.DataFrame({
                'Year': get_col_data(df_raw_indiv, ['Year', 'year'], 4).astype(str).str.replace(r'\.0$', '', regex=True).str.strip(),
                'Month': pd.to_numeric(get_col_data(df_raw_indiv, ['Month', 'month'], 5), errors='coerce').fillna(0),
                'SalesRep': get_col_data(df_raw_indiv, ['Sales'], 0).astype(str).str.strip(),
                'Group': get_col_data(df_raw_indiv, ['Group1', 'Group'], 6).apply(normalize_grp),
                'Target': clean_num(get_col_data(df_raw_indiv, ['Value', 'IndividualPlanValue'], 3))
            })
            df_indiv = df_indiv[(df_indiv['Year'] != '') & (pd.to_numeric(df_indiv['Year'], errors='coerce') > 2000) & (df_indiv['SalesRep'] != 'nan')]
            data['indiv_norm'] = df_indiv

            # --- 4. โหลดไฟล์ INV PLAN ---
            df_raw_invplan = pd.read_csv(get_gdrive_direct_url(gdrive_files['inv_plan']), header=0)
            df_invplan = pd.DataFrame({
                'Year': get_col_data(df_raw_invplan, ['Year', 'year'], 5).astype(str).str.replace(r'\.0$', '', regex=True).str.strip(),
                'Month': pd.to_numeric(get_col_data(df_raw_invplan, ['Month', 'month'], 6), errors='coerce').fillna(0),
                'Group': get_col_data(df_raw_invplan, ['Group', 'group', 'ทีมขาย'], 0).apply(normalize_grp),
                'PlanSales': clean_num(get_col_data(df_raw_invplan, ['INV Plan Sales Value'], 2)),
                'PlanAcc': clean_num(get_col_data(df_raw_invplan, ['INV Plan Account Value'], 3))
            })
            df_invplan = df_invplan[(df_invplan['Year'] != '') & (pd.to_numeric(df_invplan['Year'], errors='coerce') > 2000)]
            data['invplan_norm'] = df_invplan

            # --- 5. โหลดไฟล์ INV DATA ---
            df_raw_inv = pd.read_csv(get_gdrive_direct_url(gdrive_files['inv']), header=0)
            raw_dates = get_col_data(df_raw_inv, ['วันที่','Date','inv date'], 5)
            parsed_dates = pd.to_datetime(raw_dates, errors='coerce', dayfirst=True)
            val = clean_num(get_col_data(df_raw_inv, ['ยอดสุทธิก่อนภาษี','ยอดสุทธิ','ยอดขาย','amount','value'], 12))
            cost = clean_num(get_col_data(df_raw_inv, ['ต้นทุน','cost'], 13))
            prof_raw = clean_num(get_col_data(df_raw_inv, ['กำไร','profit','margin'], -1))
            
            profit = np.where((prof_raw == 0) & (val > 0), val - cost, prof_raw)
            profit = np.where(profit < 0, 0, profit)

            df_inv = pd.DataFrame({
                'Year': parsed_dates.dt.year.fillna(2026).astype(int).astype(str),
                'Month': parsed_dates.dt.month.fillna(1).astype(int),
                'Group': get_col_data(df_raw_inv, ['ทีมขาย','Group'], 11).apply(normalize_grp),
                'Value': val,
                'Profit': profit,
                'InvNo': get_col_data(df_raw_inv, ['เลขที่','DocNo','Invoice'], 4).astype(str).str.strip(),
                'RefSoNumber': get_col_data(df_raw_inv, ['โครงการ','Project','SO'], 14).astype(str).str.strip()
            })
            df_inv = df_inv[(df_inv['Year'] != '') & (df_inv['InvNo'] != '') & (df_inv['InvNo'] != 'nan')]
            data['inv_norm'] = df_inv

            # --- 6. โหลดไฟล์ SOI DATA ---
            df_raw_soi = pd.read_csv(get_gdrive_direct_url(gdrive_files['soi']), header=0)
            
            try:
                parsed_soi_dates = pd.to_datetime(df_raw_soi.iloc[:, 3], errors='coerce')
                valid_soi_dates = parsed_soi_dates[parsed_soi_dates <= pd.Timestamp.now() + pd.Timedelta(days=365)]
                data['latest_soi'] = valid_soi_dates.max() if not valid_soi_dates.empty else pd.NaT
            except:
                data['latest_soi'] = pd.NaT
            
            raw_type = get_col_data(df_raw_soi, ['PdTypeName', 'Type'], 3).astype(str).str.strip()
            norm_type = raw_type.apply(lambda x: x if x in ["สินค้ากึ่งสำเร็จรูป", "สินค้าสำเร็จรูป", "บริการ"] else "รายได้อื่นๆ")
            df_soi = pd.DataFrame({
                'JobNo': get_col_data(df_raw_soi, ['JobNo'], 0).astype(str).str.strip(),
                'DeliveryDate': get_col_data(df_raw_soi, ['DeliveryDueDate', 'Delivery Date'], 5).astype(str).str.strip(),
                'PdCode': get_col_data(df_raw_soi, ['PdCode', 'Item Code'], 1).astype(str).str.strip(),
                'PdName': get_col_data(df_raw_soi, ['PdName', 'Description'], 2).astype(str).str.strip(),
                'PdTypeName': norm_type,
                'Qty': get_col_data(df_raw_soi, ['Qty', 'Quantity'], 4) 
            })
            data['soi_norm'] = df_soi

            # ==========================================
            # 🚀 PRE-COMPUTATION
            # ==========================================
            data['soi_del_map'] = df_soi[df_soi['DeliveryDate'] != ''].groupby('JobNo')['DeliveryDate'].first().to_dict()
            data['inv_lookup'] = df_inv.groupby('RefSoNumber').agg(
                invNos=('InvNo', lambda x: ', '.join(set([str(i) for i in x if str(i) != 'nan' and str(i) != '']))),
                invTotalVal=('Value', 'sum')
            ).to_dict('index')

            soi_map_dict = {}
            for row in df_soi.itertuples(index=False):
                j_no = row.JobNo
                if j_no not in soi_map_dict: soi_map_dict[j_no] = []
                soi_map_dict[j_no].append({
                    'pdCode': str(getattr(row, 'PdCode', '')).strip(),
                    'pdName': str(getattr(row, 'PdName', '')).strip(),
                    'pdTypeName': str(getattr(row, 'PdTypeName', '')).strip(),
                    'qty': getattr(row, 'Qty', 0)
                })
            data['soi_map'] = soi_map_dict
            data['cust_dates'] = df_so.dropna(subset=['SODate']).groupby('Customer')['SODate'].apply(list).to_dict()

            st.sidebar.success("✅ โหลดและปรับจูนข้อมูลเสร็จสิ้น")
            return data, True
            
    except Exception as e:
        st.sidebar.error(f"❌ โหลดข้อมูลผิดพลาด: ระบบแสดงข้อมูลจำลองชั่วคราว ({str(e)})")
        return generate_mock_data(), False

def generate_mock_data():
    np.random.seed(42)
    months = np.random.randint(1, 13, 100)
    df_plan = pd.DataFrame({'Year': '2026', 'Month': months, 'Group': 'A', 'Target': np.random.randint(1e6, 5e6, 100), 'Product': ['VK', 'OT', 'GP'][np.random.randint(0,3)]})
    df_so = pd.DataFrame({'Year': '2026', 'Month': months, 'Group': 'A', 'Actual': np.random.randint(5e5, 6e6, 100), 
                          'Customer': ['Cust '+str(i) for i in np.random.randint(1,20,100)], 
                          'Industry': ['IND '+str(i) for i in np.random.randint(1,5,100)],
                          'Margin': np.random.randint(1e5, 5e5, 100),
                          'SalesRep': ['Rep '+str(i) for i in np.random.randint(1,5,100)],
                          'Product': ['VK', 'OT', 'GP'][np.random.randint(0,3)],
                          'SONumber': ['SO'+str(i) for i in range(100)],
                          'RegYear': '2026', 'RegMonth': months,
                          'QuotationNo': ['QT'+str(i) for i in range(100)],
                          'SODate': pd.to_datetime('2026-01-01')})
    df_indiv = pd.DataFrame({'Year': '2026', 'Month': months, 'SalesRep': ['Rep '+str(i) for i in np.random.randint(1,5,100)], 'Group': 'A', 'Target': np.random.randint(5e5, 2e6, 100)})
    df_invplan = pd.DataFrame({'Year': '2026', 'Month': months, 'Group': 'A', 'PlanSales': np.random.randint(1e6, 5e6, 100), 'PlanAcc': np.random.randint(8e5, 4e6, 100)})
    df_inv = pd.DataFrame({'Year': '2026', 'Month': months, 'Group': 'A', 'Value': np.random.randint(5e5, 6e6, 100), 'Profit': np.random.randint(1e5, 5e5, 100), 'InvNo': ['INV'+str(i) for i in range(100)], 'RefSoNumber': ['SO'+str(i) for i in range(100)]})
    df_soi = pd.DataFrame({'JobNo': ['SO'+str(i) for i in range(100)], 'DeliveryDate': [f"15/{m}/2026" for m in months], 'PdCode': [f"ITEM-{i}" for i in range(100)], 'PdName': [f"Product Description {i}" for i in range(100)], 'PdTypeName': ['สินค้าสำเร็จรูป' for i in range(100)], 'Qty': [np.random.randint(1, 100) for _ in range(100)]})
    
    soi_map_dict = {}
    for row in df_soi.itertuples():
        j_no = row.JobNo
        if j_no not in soi_map_dict: soi_map_dict[j_no] = []
        soi_map_dict[j_no].append({'pdCode': row.PdCode, 'pdName': row.PdName, 'pdTypeName': row.PdTypeName, 'qty': row.Qty})
        
    return {'plan_norm': df_plan, 'so_norm': df_so, 'indiv_norm': df_indiv, 'invplan_norm': df_invplan, 'inv_norm': df_inv, 'soi_norm': df_soi,
            'soi_del_map': {}, 'inv_lookup': {}, 'soi_map': soi_map_dict, 'cust_dates': {}, 
            'latest_so': pd.Timestamp('2026-04-15'), 'latest_soi': pd.Timestamp('2026-04-16')}

# โหลดข้อมูลหลัก
data, is_real_data = load_data()
df_plan_all = data['plan_norm']
df_so_all = data['so_norm']
df_indiv_all = data['indiv_norm']
df_invplan_all = data['invplan_norm']
df_inv_all = data['inv_norm']
df_soi_all = data['soi_norm']

soi_del_map = data.get('soi_del_map', {})
inv_lookup = data.get('inv_lookup', {})
soi_map = data.get('soi_map', {})
cust_dates = data.get('cust_dates', {})

latest_so = data.get('latest_so', pd.NaT)
latest_soi = data.get('latest_soi', pd.NaT)

str_so = format_exact_th_date(latest_so) if pd.notna(latest_so) else "ไม่ระบุ"
str_soi = format_exact_th_date(latest_soi) if pd.notna(latest_soi) else "ไม่ระบุ"

st.markdown(f'''
    <div style="margin-top: -1rem; margin-bottom: 1.5rem; font-family: 'Canva Sans', 'Sarabun', sans-serif; display: flex; align-items: baseline; flex-wrap: wrap;">
        <span style="color: #2B3467; font-size: 24px; font-weight: bold; margin-right: 12px;">📊 Siamraj Sales Dashboard v3.0</span>
        <span style="font-size: 14px; color: #64748b; font-weight: 500;">
            (สถานะอัปเดตข้อมูล: รายการ SO ล่าสุด {str_so} &nbsp;|&nbsp; รายการ SOI ล่าสุด {str_soi})
        </span>
    </div>
''', unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR (FILTERS)
# ==========================================

# คำนวณปีและเดือนปัจจุบันสำหรับตั้งค่าเริ่มต้น
current_year = str(pd.Timestamp.now().year)
current_month = pd.Timestamp.now().month

with st.sidebar:
    st.markdown('<h2 style="color:#1e293b; font-size:16px; margin-bottom:10px;">🎛️ ตัวกรองข้อมูล (Filters)</h2>', unsafe_allow_html=True)
    
    available_years = sorted(list(set(df_plan_all['Year'].unique()) | set(df_so_all['Year'].unique())), reverse=True)
    year_options = ['All'] + available_years
    
    # ตั้งค่าปีเริ่มต้นให้เป็นปีล่าสุดหากไม่พบปีปัจจุบัน
    default_year_idx = 0 # 'All' คือ index 0
    if current_year in available_years:
        default_year_idx = year_options.index(current_year)
    elif len(available_years) > 0:
        default_year_idx = 1 # Default to the most recent year available
        
    st.markdown('<div style="font-weight:600; color:#475569; font-size:13px; margin-bottom:4px; margin-top:12px;"><i class="fa-solid fa-calendar-days" style="margin-right:5px;"></i>เลือกปี (YEAR)</div>', unsafe_allow_html=True)
    selected_year = st.radio("Year", year_options, index=default_year_idx, horizontal=True, label_visibility="collapsed")
    
    st.markdown('<div style="font-weight:600; color:#475569; font-size:13px; margin-bottom:4px; margin-top:12px;"><i class="fa-solid fa-users" style="margin-right:5px;"></i>เลือกกลุ่ม (GROUP)</div>', unsafe_allow_html=True)
    selected_group = st.radio("Group", ["All", "A", "B", "C", "D", "R", "COM", "PD"], horizontal=True, label_visibility="collapsed")
    
    st.markdown('<div style="font-weight:600; color:#475569; font-size:13px; margin-bottom:4px; margin-top:12px;"><i class="fa-solid fa-clock" style="margin-right:5px;"></i>เลือกเดือน (MONTH)</div>', unsafe_allow_html=True)
    
    month_opts = ["All"] + [str(i) for i in range(1, 13)]
    default_month_idx = current_month 
    sel_m = st.radio("Month", month_opts, index=default_month_idx, horizontal=True, label_visibility="collapsed")
    
    if sel_m == "All":
        selected_month = list(range(1, 13))
    else:
        selected_month = [int(sel_m)]
    
    st.divider()

# ==========================================
# 5. DATA AGGREGATION LOGIC
# ==========================================
df_plan_year = df_plan_all.copy()
df_so_year = df_so_all.copy()
df_indiv_year = df_indiv_all.copy()
df_invplan_year = df_invplan_all.copy()
df_inv_year = df_inv_all.copy()

if selected_year != 'All':
    df_plan_year = df_plan_year[df_plan_year['Year'] == selected_year]
    df_so_year = df_so_year[df_so_year['Year'] == selected_year]
    df_indiv_year = df_indiv_year[df_indiv_year['Year'] == selected_year]
    df_invplan_year = df_invplan_year[df_invplan_year['Year'] == selected_year]
    df_inv_year = df_inv_year[df_inv_year['Year'] == selected_year]

if selected_group != "All":
    df_plan_year = df_plan_year[df_plan_year['Group'] == selected_group]
    df_so_year = df_so_year[df_so_year['Group'] == selected_group]
    df_indiv_year = df_indiv_year[df_indiv_year['Group'] == selected_group]
    df_invplan_year = df_invplan_year[df_invplan_year['Group'] == selected_group]
    df_inv_year = df_inv_year[df_inv_year['Group'] == selected_group]

if not selected_month: selected_month = list(range(1, 13))
max_m = max(selected_month)

period_plan = df_plan_year[df_plan_year['Month'].isin(selected_month)]['Target'].sum()
period_actual = df_so_year[df_so_year['Month'].isin(selected_month)]['Actual'].sum()
period_margin = df_so_year[df_so_year['Month'].isin(selected_month)]['Margin'].sum()

ytd_plan = df_plan_year[df_plan_year['Month'] <= max_m]['Target'].sum()
ytd_actual = df_so_year[df_so_year['Month'] <= max_m]['Actual'].sum()
ytd_margin = df_so_year[df_so_year['Month'] <= max_m]['Margin'].sum()

annual_plan = df_plan_year['Target'].sum()
annual_actual = df_so_year['Actual'].sum()
annual_margin = df_so_year['Margin'].sum()

def calc_kpi(a, p, m):
    ach = (a / p * 100) if p > 0 else 0
    mg = (m / a * 100) if a > 0 else 0
    foc = max(0, p - a)
    return ach, mg, foc

p_ach, p_mg, p_foc = calc_kpi(period_actual, period_plan, period_margin)
y_ach, y_mg, y_foc = calc_kpi(ytd_actual, ytd_plan, ytd_margin)
a_ach, a_mg, a_foc = calc_kpi(annual_actual, annual_plan, annual_margin)

s_year = f"ปี {selected_year}" if selected_year != 'All' else "ทุกปีรวมกัน"
s_grp = f"กลุ่ม {selected_group}" if selected_group != "All" else "ทุกกลุ่ม"

if len(selected_month) == 12: s_month_txt = "ทุกเดือน"
elif len(selected_month) == 1: s_month_txt = f"เดือน{TH_MONTHS_FULL[selected_month[0]]}"
elif selected_month == [1,2,3]: s_month_txt = "Q1 (ม.ค.-มี.ค.)"
elif selected_month == [4,5,6]: s_month_txt = "Q2 (เม.ย.-มิ.ย.)"
elif selected_month == [7,8,9]: s_month_txt = "Q3 (ก.ค.-ก.ย.)"
elif selected_month == [10,11,12]: s_month_txt = "Q4 (ต.ค.-ธ.ค.)"
else: s_month_txt = "หลายเดือน"

hdr_period = s_month_txt
hdr_ytd = f"สะสม (ม.ค. - {TH_MONTHS[max_m]})" if max_m > 1 else "สะสม (ม.ค.)"
hdr_year = f"ปี {selected_year}" if selected_year != 'All' else "ทุกปีรวมกัน"

sub_period = f"{s_month_txt} | {s_grp} | {s_year}"
sub_ytd = f"สะสม ม.ค.-{TH_MONTHS[max_m]} | {s_grp} | {s_year}"
sub_annual = f"รวมทั้งปี | {s_grp} | {s_year}"
sub_group_only = f"{s_grp} | {s_year}"

def metric_card(col, subtitle, plan, actual, profit, customers, so_count):
    achieve = (actual / plan * 100) if plan > 0 else 0
    margin_pct = (profit / actual * 100) if actual > 0 else 0
    gap = actual - plan
    gap_color = "#00b862" if gap >= 0 else "#dc2626"
    gap_sign = "+" if gap > 0 else ""
    
    html = f"""
<div style="background-color: white; border: 1px solid #d8b4fe; border-radius: 8px; padding: 24px 16px; box-shadow: 0 2px 6px rgba(107, 33, 168, 0.05); font-family: 'Arimo', 'Canva Sans', 'Sarabun', sans-serif;">
<div style="text-align: center; margin-bottom: 20px;">
<span style="background-color: #f3e8ff; color: #6b21a8; padding: 6px 16px; border-radius: 6px; font-size: 13px; font-weight: 700;">{subtitle}</span>
</div>
<div style="text-align: center; padding-bottom: 20px; border-bottom: 1px solid #e9d5ff; margin-bottom: 20px;">
<div style="font-size: 28px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(plan)}</div>
<div style="font-size: 13px; color: #6b7280; font-style: italic; margin-top: 4px;">Plan</div>
</div>
<div style="display: flex; text-align: center;">
<div style="flex: 1.1; border-right: 1px solid #e9d5ff; padding: 0 4px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="margin-bottom: 20px;">
<div style="font-size: 24px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(actual)}</div>
<div style="font-size: 12px; color: #6b7280; font-style: italic;">SaleActual</div>
</div>
<div style="display: flex; justify-content: space-around;">
<div>
<div style="font-size: 20px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(customers)}</div>
<div style="font-size: 12px; color: #6b7280; font-style: italic;">Customers</div>
</div>
<div>
<div style="font-size: 20px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(so_count)}</div>
<div style="font-size: 12px; color: #6b7280; font-style: italic;">SO Count:</div>
</div>
</div>
</div>
<div style="flex: 0.9; border-right: 1px solid #e9d5ff; padding: 0 4px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="margin-bottom: 20px;">
<div style="font-size: 24px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(achieve, 1)}%</div>
<div style="font-size: 12px; color: #6b7280; font-style: italic;">Achievement</div>
</div>
<div>
<div style="font-size: 22px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(margin_pct, 1)}%</div>
<div style="font-size: 12px; color: #6b7280; font-style: italic;">Margin</div>
</div>
</div>
<div style="flex: 1; padding: 0 4px; display: flex; flex-direction: column; justify-content: space-between;">
<div style="margin-bottom: 20px;">
<div style="font-size: 24px; font-weight: 800; color: {gap_color}; line-height: 1.2;">{gap_sign}{safe_fmt(gap)}</div>
<div style="font-size: 12px; color: {gap_color}; font-style: italic;">Keep Focus</div>
</div>
<div>
<div style="font-size: 22px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(profit)}</div>
<div style="font-size: 12px; color: #6b7280; font-style: italic;">Profit</div>
</div>
</div>
</div>
</div>
"""
    col.markdown(html, unsafe_allow_html=True)

def mk_cell(p, a, is_group=False):
    gap = max(0, p - a)
    pct = safe_pct(a, p)
    nc = "color: #ef4444;" if gap > 0 else "color: #10b981;"
    bg = "background-color: #f8fafc;" if is_group else "background-color: white;"
    c1 = "#334155" if is_group else "#64748b"
    c2 = "#3730a3" if is_group else "#4338ca"
    fz_val = "font-size: 15px;" if is_group else "font-size: 14px;"
    fz_pct = "font-size: 14px;" if is_group else "font-size: 13px;"
    
    icon = ""
    if p > 0:
        if a >= p:
            icon = ' <span style="font-size: 14px;" title="บรรลุเป้าหมาย">✅</span>'
        else:
            icon = ' <span style="font-size: 14px;" title="ต่ำกว่าเป้าหมาย">🔻</span>'

    return f'<td style="{bg} text-align: right; color: {c1}; {fz_val}">{safe_fmt(p)}</td><td style="{bg} text-align: right; color: {c2}; font-weight: bold; {fz_val}">{safe_fmt(a)}</td><td style="{bg} text-align: center; {fz_pct}">{pct}{icon}</td><td style="{bg} {nc} text-align: right; font-weight: bold; border-right: 1px solid #e2e8f0; {fz_val}">{safe_fmt(gap)}</td>'

# ==========================================
# 6. MAIN DASHBOARD TABS
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📈 สรุปผลภาพรวม", 
    "📊 สรุปผลรายไตรมาส",
    "📉 แนวโน้ม & Top 10",
    "🧾 สรุปผลอินวอยซ์", 
    "🚚 แผนจัดส่ง",
    "🔎 ส่องรายละเอียดงาน",
    "📇 ประวัติลูกค้า",
    "🚨 ลูกค้าที่ห่างหาย"
])

with tab1:
    st.markdown("""
        <div style="margin-bottom: 24px; font-family: 'Sarabun', sans-serif;">
            <span style="font-size: 20px; font-weight: bold; color: #2B3467;">📈 Performance Summary</span> 
            <span style="font-size: 14px; color: #64748b;">| สรุปผลภาพรวมความสำเร็จและเป้าหมายเปรียบเทียบกับยอดขายจริง</span>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    p_cust = df_so_year[df_so_year['Month'].isin(selected_month)]['Customer'].nunique()
    p_so = df_so_year[df_so_year['Month'].isin(selected_month)]['SONumber'].nunique()
    y_cust = df_so_year[df_so_year['Month'] <= max_m]['Customer'].nunique()
    y_so = df_so_year[df_so_year['Month'] <= max_m]['SONumber'].nunique()
    a_cust = df_so_year['Customer'].nunique()
    a_so = df_so_year['SONumber'].nunique()

    metric_card(col1, sub_period, period_plan, period_actual, period_margin, p_cust, p_so)
    metric_card(col2, sub_ytd, ytd_plan, ytd_actual, ytd_margin, y_cust, y_so)
    metric_card(col3, sub_annual, annual_plan, annual_actual, annual_margin, a_cust, a_so)
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    if 'show_group_only' not in st.session_state: st.session_state.show_group_only = False
    def toggle_group_view(): st.session_state.show_group_only = not st.session_state.show_group_only

    col_title, col_btn = st.columns([7, 3])
    with col_title: st.markdown('<h3 style="color: #0f766e; font-size: 15px; margin-bottom: 0; font-family: \'Sarabun\', sans-serif;">👤 เปรียบเทียบเป้าหมาย vs ยอดขายรายบุคคล</h3>', unsafe_allow_html=True)
    with col_btn: st.button("ย่อดูเฉพาะรายกลุ่ม (Group Only)" if not st.session_state.show_group_only else "ขยายดูรายบุคคล (Show All)", on_click=toggle_group_view, use_container_width=True)

    all_reps = pd.concat([df_so_year['SalesRep'], df_indiv_year['SalesRep']]).unique()
    rep_data = []
    for rep in all_reps:
        s_data = df_so_year[df_so_year['SalesRep'] == rep]
        p_data = df_indiv_year[df_indiv_year['SalesRep'] == rep]
        group = p_data['Group'].iloc[0] if not p_data.empty else (s_data['Group'].iloc[0] if not s_data.empty else 'Others')
        mP = p_data[p_data['Month'].isin(selected_month)]['Target'].sum()
        mA = s_data[s_data['Month'].isin(selected_month)]['Actual'].sum()
        yP = p_data[p_data['Month'] <= max_m]['Target'].sum()
        yA = s_data[s_data['Month'] <= max_m]['Actual'].sum()
        aP = p_data['Target'].sum()
        aA = s_data['Actual'].sum()
        if aP > 0 or aA > 0: rep_data.append({'SalesRep': rep, 'Group': group, 'mP': mP, 'mA': mA, 'yP': yP, 'yA': yA, 'aP': aP, 'aA': aA})

    df_rep_summary = pd.DataFrame(rep_data)

    ht_parts = []
    ht_parts.append(f'<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05);"><table class="custom-table"><thead><tr><th rowspan="2" style="text-align: left; background-color: white; font-size: 14px;">Group / Sales Representative</th><th colspan="4" style="font-size: 14px; text-transform: uppercase;">{hdr_period}</th><th colspan="4" style="font-size: 14px; text-transform: uppercase;">{hdr_ytd}</th><th colspan="4" style="border-right: none; font-size: 14px; text-transform: uppercase;">{hdr_year}</th></tr><tr style="font-size: 12px;"><th class="text-right">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444;">Need</th><th class="text-right">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444;">Need</th><th class="text-right">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444; border-right: none;">Need</th></tr></thead><tbody>')
    
    t_mP = t_mA = t_yP = t_yA = t_aP = t_aA = 0
    group_order = ['A', 'B', 'C', 'D', 'R', 'COM', 'PD', 'Others']

    if not df_rep_summary.empty:
        for g_name in sorted(df_rep_summary['Group'].unique(), key=lambda x: group_order.index(x) if x in group_order else 99):
            g_df = df_rep_summary[df_rep_summary['Group'] == g_name]
            g_mP = g_df['mP'].sum(); g_mA = g_df['mA'].sum(); g_yP = g_df['yP'].sum(); g_yA = g_df['yA'].sum(); g_aP = g_df['aP'].sum(); g_aA = g_df['aA'].sum()
            t_mP += g_mP; t_mA += g_mA; t_yP += g_yP; t_yA += g_yA; t_aP += g_aP; t_aA += g_aA
            ht_parts.append(f'<tr class="group-row"><td style="border-right: 1px solid #e2e8f0; background-color: #f8fafc; font-size: 15px;">GROUP {g_name}</td>{mk_cell(g_mP, g_mA, True)}{mk_cell(g_yP, g_yA, True)}{mk_cell(g_aP, g_aA, True).replace("border-right: 1px solid #e2e8f0;", "")}</tr>')
            if not st.session_state.show_group_only:
                for row in g_df.sort_values('aA', ascending=False).itertuples(index=False):
                    ht_parts.append(f'<tr><td style="padding-left: 20px; border-right: 1px solid #e2e8f0; font-size: 14px;">{row.SalesRep}</td>{mk_cell(row.mP, row.mA)}{mk_cell(row.yP, row.yA)}{mk_cell(row.aP, row.aA).replace("border-right: 1px solid #e2e8f0;", "")}</tr>')

    ht_parts.append(f'</tbody><tfoot><tr style="background-color: #f1f5f9; font-weight: bold; color: #1e293b;"><td style="border-right: 1px solid #e2e8f0; text-transform: uppercase; font-size: 15px;">Total</td>{mk_cell(t_mP, t_mA, True)}{mk_cell(t_yP, t_yA, True)}{mk_cell(t_aP, t_aA, True).replace("border-right: 1px solid #e2e8f0;", "")}</tr></tfoot></table></div>')
    st.markdown("".join(ht_parts), unsafe_allow_html=True)

    if 'show_prod_only' not in st.session_state: st.session_state.show_prod_only = False
    def toggle_prod_view(): st.session_state.show_prod_only = not st.session_state.show_prod_only

    col_title_prod, col_btn_prod = st.columns([7, 3])
    with col_title_prod: st.markdown('<h3 style="color: #4338ca; font-size: 15px; margin-bottom: 0; font-family: \'Sarabun\', sans-serif;">📦 รายละเอียดตามผลิตภัณฑ์ (Product Detail)</h3>', unsafe_allow_html=True)
    with col_btn_prod: st.button("ย่อดูเฉพาะหลัก (Main Only)" if not st.session_state.show_prod_only else "ขยายดูรายกลุ่ม (Show All)", on_click=toggle_prod_view, use_container_width=True, key="btn_prod")

    p_map = { "LC": "LC & CK", "CK": "LC & CK", "OM": "OM & JC", "JC": "OM & JC", "OT": "OT/PIGGING", "VP": "OT/PIGGING", "SE": "SE & KW", "KW": "SE & KW" }
    def get_mapped_prod(p): return p_map.get(str(p).strip(), str(p).strip()) if pd.notna(p) else "Unknown"

    prod_map = {}
    for row in df_plan_year.itertuples(index=False):
        p = get_mapped_prod(row.Product); g = row.Group if pd.notna(row.Group) else "Others"; v = row.Target; m = row.Month
        if p not in prod_map: prod_map[p] = {'pP':0, 'pA':0, 'yP':0, 'yA':0, 'aP':0, 'aA':0, 'groups': {}}
        if g not in prod_map[p]['groups']: prod_map[p]['groups'][g] = {'pP':0, 'pA':0, 'yP':0, 'yA':0, 'aP':0, 'aA':0}
        if m in selected_month: prod_map[p]['pP'] += v; prod_map[p]['groups'][g]['pP'] += v
        if m <= max_m: prod_map[p]['yP'] += v; prod_map[p]['groups'][g]['yP'] += v
        prod_map[p]['aP'] += v; prod_map[p]['groups'][g]['aP'] += v

    for row in df_so_year.itertuples(index=False):
        p = get_mapped_prod(row.Product); g = row.Group if pd.notna(row.Group) else "Others"; v = row.Actual; m = row.Month
        if p not in prod_map: prod_map[p] = {'pP':0, 'pA':0, 'yP':0, 'yA':0, 'aP':0, 'aA':0, 'groups': {}}
        if g not in prod_map[p]['groups']: prod_map[p]['groups'][g] = {'pP':0, 'pA':0, 'yP':0, 'yA':0, 'aP':0, 'aA':0}
        if m in selected_month: prod_map[p]['pA'] += v; prod_map[p]['groups'][g]['pA'] += v
        if m <= max_m: prod_map[p]['yA'] += v; prod_map[p]['groups'][g]['yA'] += v
        prod_map[p]['aA'] += v; prod_map[p]['groups'][g]['aA'] += v

    hp_parts = []
    hp_parts.append(f'<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05);"><table class="custom-table"><thead><tr><th rowspan="2" style="text-align: left; background-color: white; font-size: 14px;">Product / Group</th><th colspan="4" style="font-size: 14px; text-transform: uppercase;">{hdr_period}</th><th colspan="4" style="font-size: 14px; text-transform: uppercase;">{hdr_ytd}</th><th colspan="4" style="border-right: none; font-size: 14px; text-transform: uppercase;">{hdr_year}</th></tr><tr style="font-size: 12px;"><th class="text-right">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444;">Need</th><th class="text-right">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444;">Need</th><th class="text-right">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444; border-right: none;">Need</th></tr></thead><tbody>')
    gT_prod = {'pp':0, 'pa':0, 'yp':0, 'ya':0, 'ap':0, 'aa':0}
    sorted_prods = sorted(prod_map.keys(), key=lambda x: prod_map[x]['aP'], reverse=True)

    for prod in sorted_prods:
        d = prod_map[prod]
        if d['aP'] == 0 and d['aA'] == 0: continue
        gT_prod['pp'] += d['pP']; gT_prod['pa'] += d['pA']; gT_prod['yp'] += d['yP']; gT_prod['ya'] += d['yA']; gT_prod['ap'] += d['aP']; gT_prod['aa'] += d['aA']
        has_sub = len(d['groups']) > 0
        hp_parts.append(f'<tr class="group-row bg-slate-200"><td style="border-right: 1px solid #e2e8f0; background-color: #f8fafc; color: #3730a3; font-weight: bold; font-size: 15px;"><span style="display:inline-block; width:12px;"></span>🔹 {prod}</td>{mk_cell(d["pP"], d["pA"], True)}{mk_cell(d["yP"], d["yA"], True)}{mk_cell(d["aP"], d["aA"], True).replace("border-right: 1px solid #e2e8f0;", "")}</tr>')
        if has_sub and not st.session_state.show_prod_only:
            sorted_groups = sorted(d['groups'].keys(), key=lambda x: group_order.index(x) if x in group_order else 99)
            for g_name in sorted_groups:
                gD = d['groups'][g_name]
                if gD['aP'] == 0 and gD['aA'] == 0: continue
                hp_parts.append(f'<tr><td style="padding-left: 28px; border-right: 1px solid #e2e8f0; font-size: 14px; color: #64748b;">GROUP {g_name}</td>{mk_cell(gD["pP"], gD["pA"])}{mk_cell(gD["yP"], gD["yA"])}{mk_cell(gD["aP"], gD["aA"]).replace("border-right: 1px solid #e2e8f0;", "")}</tr>')
                
    hp_parts.append(f'</tbody><tfoot><tr style="background-color: #e0e7ff; font-weight: bold; color: #312e81;"><td style="border-right: 1px solid #e2e8f0; text-transform: uppercase; font-size: 15px;">Grand Total</td>{mk_cell(gT_prod["pp"], gT_prod["pa"], True)}{mk_cell(gT_prod["yp"], gT_prod["ya"], True)}{mk_cell(gT_prod["ap"], gT_prod["aa"], True).replace("border-right: 1px solid #e2e8f0;", "")}</tr></tfoot></table></div>')
    st.markdown("".join(hp_parts), unsafe_allow_html=True)

with tab2:
    st.markdown("<div style='margin-bottom: 24px;'><span style='font-size: 20px; font-weight: bold; color: #2B3467;'>📊 Quarterly Performance Summary</span> <span style='font-size: 14px; color: #64748b;'>| สรุปผลภาพรวมความสำเร็จแยกตามรายไตรมาส (Q1 - Q4) ของปีที่เลือก</span></div>", unsafe_allow_html=True)
    
    q_cols = st.columns(4)
    
    quarters_map = {
        'Q1': [1, 2, 3],
        'Q2': [4, 5, 6],
        'Q3': [7, 8, 9],
        'Q4': [10, 11, 12]
    }
    
    q_chart_data = []

    for i, (q_name, q_months) in enumerate(quarters_map.items()):
        q_plan = df_plan_year[df_plan_year['Month'].isin(q_months)]['Target'].sum()
        q_so = df_so_year[df_so_year['Month'].isin(q_months)]
        
        q_actual = q_so['Actual'].sum()
        q_profit = q_so['Margin'].sum()
        q_cust = q_so['Customer'].nunique()
        q_so_cnt = q_so['SONumber'].nunique()
        
        subtitle = f"ไตรมาส {q_name} | {s_grp} | {s_year}"
        
        metric_card(q_cols[i], subtitle, q_plan, q_actual, q_profit, q_cust, q_so_cnt)
        
        q_chart_data.append({
            'Quarter': q_name,
            'Plan/Target': q_plan,
            'Actual': q_actual
        })

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    if 'show_group_only_q' not in st.session_state: st.session_state.show_group_only_q = False
    def toggle_group_view_q(): st.session_state.show_group_only_q = not st.session_state.show_group_only_q

    col_title_q, col_btn_q = st.columns([7, 3])
    # ขยายขนาดฟอนต์เป็น 18px
    with col_title_q: st.markdown('<h3 style="color: #0f766e; font-size: 18px; margin-bottom: 0; padding-top: 5px; font-family: \'Sarabun\', sans-serif;">👤 เปรียบเทียบเป้าหมาย vs ยอดขายรายบุคคล (ไตรมาส)</h3>', unsafe_allow_html=True)
    with col_btn_q: st.button("ย่อดูเฉพาะรายกลุ่ม (Group Only)" if not st.session_state.show_group_only_q else "ขยายดูรายบุคคล (Show All)", on_click=toggle_group_view_q, use_container_width=True, key="btn_group_q")

    all_reps_q = pd.concat([df_so_year['SalesRep'], df_indiv_year['SalesRep']]).unique()
    rep_data_q = []
    for rep in all_reps_q:
        s_data = df_so_year[df_so_year['SalesRep'] == rep]
        p_data = df_indiv_year[df_indiv_year['SalesRep'] == rep]
        group = p_data['Group'].iloc[0] if not p_data.empty else (s_data['Group'].iloc[0] if not s_data.empty else 'Others')
        
        q_metrics = {}
        for q, mths in quarters_map.items():
            q_metrics[f'{q}_P'] = p_data[p_data['Month'].isin(mths)]['Target'].sum()
            q_metrics[f'{q}_A'] = s_data[s_data['Month'].isin(mths)]['Actual'].sum()
        
        aP = p_data['Target'].sum()
        aA = s_data['Actual'].sum()
        if aP > 0 or aA > 0: 
            rep_dict = {'SalesRep': rep, 'Group': group, 'aP': aP, 'aA': aA}
            rep_dict.update(q_metrics)
            rep_data_q.append(rep_dict)

    df_rep_summary_q = pd.DataFrame(rep_data_q)

    ht_parts_q = []
    ht_parts_q.append('<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.05);"><table class="custom-table" style="min-width: 1400px;"><thead><tr><th rowspan="2" style="text-align: left; background-color: white; font-size: 14px; position: sticky; left: 0; z-index: 2;">Group / Sales Representative</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q1</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q2</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q3</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q4</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0; border-right: none;">Total Year</th></tr><tr style="font-size: 12px;">')
    for i in range(5):
        bl = "border-left: 2px solid #e2e8f0;" if i > 0 else ""
        br = "border-right: none;" if i == 4 else ""
        ht_parts_q.append(f'<th class="text-right" style="{bl}">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444; {br}">Need</th>')
    ht_parts_q.append('</tr></thead><tbody>')
    
    def mk_cell_q(p, a, is_group=False, border_left=False, border_right_none=False, short_num=False):
        gap = max(0, p - a)
        pct = safe_pct(a, p)
        nc = "color: #ef4444;" if gap > 0 else "color: #10b981;"
        bg = "background-color: #f8fafc;" if is_group else "background-color: white;"
        c1 = "#334155" if is_group else "#64748b"
        c2 = "#3730a3" if is_group else "#4338ca"
        fz_val = "font-size: 15px;" if is_group else "font-size: 14px;"
        fz_pct = "font-size: 14px;" if is_group else "font-size: 13px;"
        
        icon = ""
        if p > 0:
            icon = ' <span style="font-size: 14px;" title="บรรลุเป้าหมาย">✅</span>' if a >= p else ' <span style="font-size: 14px;" title="ต่ำกว่าเป้าหมาย">🔻</span>'

        bl = "border-left: 2px solid #e2e8f0; " if border_left else ""
        br = "border-right: none; " if border_right_none else "border-right: 1px solid #e2e8f0; "
        
        p_str = format_num_short(p) if short_num else safe_fmt(p)
        a_str = format_num_short(a) if short_num else safe_fmt(a)
        gap_str = format_num_short(gap) if short_num else safe_fmt(gap)
        
        return f'<td style="{bg} {bl} text-align: right; color: {c1}; {fz_val}">{p_str}</td><td style="{bg} text-align: right; color: {c2}; font-weight: bold; {fz_val}">{a_str}</td><td style="{bg} text-align: center; {fz_pct}">{pct}{icon}</td><td style="{bg} {nc} text-align: right; font-weight: bold; {br} {fz_val}">{gap_str}</td>'

    t_Q = {f'Q{i}_P': 0 for i in range(1, 5)}; t_Q.update({f'Q{i}_A': 0 for i in range(1, 5)})
    t_aP = 0; t_aA = 0

    group_order = ['A', 'B', 'C', 'D', 'R', 'COM', 'PD', 'Others']

    if not df_rep_summary_q.empty:
        for g_name in sorted(df_rep_summary_q['Group'].unique(), key=lambda x: group_order.index(x) if x in group_order else 99):
            g_df = df_rep_summary_q[df_rep_summary_q['Group'] == g_name]
            g_Q = {k: g_df[k].sum() for k in t_Q.keys()}
            g_aP = g_df['aP'].sum(); g_aA = g_df['aA'].sum()
            
            for k in t_Q.keys(): t_Q[k] += g_Q[k]
            t_aP += g_aP; t_aA += g_aA
            
            row_html = f'<tr class="group-row"><td style="border-right: 1px solid #e2e8f0; background-color: #f8fafc; font-size: 15px; position: sticky; left: 0; z-index: 1;">GROUP {g_name}</td>'
            row_html += mk_cell_q(g_Q['Q1_P'], g_Q['Q1_A'], True)
            row_html += mk_cell_q(g_Q['Q2_P'], g_Q['Q2_A'], True, True)
            row_html += mk_cell_q(g_Q['Q3_P'], g_Q['Q3_A'], True, True)
            row_html += mk_cell_q(g_Q['Q4_P'], g_Q['Q4_A'], True, True)
            row_html += mk_cell_q(g_aP, g_aA, True, True, True, short_num=True)
            row_html += '</tr>'
            ht_parts_q.append(row_html)
            
            if not st.session_state.show_group_only_q:
                for row in g_df.sort_values('aA', ascending=False).itertuples(index=False):
                    r_html = f'<tr><td style="padding-left: 20px; border-right: 1px solid #e2e8f0; font-size: 14px; position: sticky; left: 0; z-index: 1; background-color: white;">{row.SalesRep}</td>'
                    r_html += mk_cell_q(row.Q1_P, row.Q1_A)
                    r_html += mk_cell_q(row.Q2_P, row.Q2_A, False, True)
                    r_html += mk_cell_q(row.Q3_P, row.Q3_A, False, True)
                    r_html += mk_cell_q(row.Q4_P, row.Q4_A, False, True)
                    r_html += mk_cell_q(row.aP, row.aA, False, True, True, short_num=True)
                    r_html += '</tr>'
                    ht_parts_q.append(r_html)

    foot_html = f'</tbody><tfoot><tr style="background-color: #f1f5f9; font-weight: bold; color: #1e293b;"><td style="border-right: 1px solid #e2e8f0; text-transform: uppercase; font-size: 15px; position: sticky; left: 0; z-index: 1;">Total</td>'
    foot_html += mk_cell_q(t_Q['Q1_P'], t_Q['Q1_A'], True)
    foot_html += mk_cell_q(t_Q['Q2_P'], t_Q['Q2_A'], True, True)
    foot_html += mk_cell_q(t_Q['Q3_P'], t_Q['Q3_A'], True, True)
    foot_html += mk_cell_q(t_Q['Q4_P'], t_Q['Q4_A'], True, True)
    foot_html += mk_cell_q(t_aP, t_aA, True, True, True, short_num=True)
    foot_html += '</tr></tfoot></table></div>'
    ht_parts_q.append(foot_html)
    
    st.markdown("".join(ht_parts_q), unsafe_allow_html=True)


    # PRODUCT TABLE FOR QUARTERS
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    if 'show_prod_only_q' not in st.session_state: st.session_state.show_prod_only_q = False
    def toggle_prod_view_q(): st.session_state.show_prod_only_q = not st.session_state.show_prod_only_q

    col_title_prod_q, col_btn_prod_q = st.columns([7, 3])
    # ขยายขนาดฟอนต์และเปลี่ยนรูปแบบฟอนต์เป็น Sarabun
    with col_title_prod_q: st.markdown('<h3 style="color: #4338ca; font-size: 18px; margin-bottom: 0; padding-top: 5px; font-family: \'Sarabun\', sans-serif;">📦 รายละเอียดตามผลิตภัณฑ์ (Product Detail) (ไตรมาส)</h3>', unsafe_allow_html=True)
    with col_btn_prod_q: st.button("ย่อดูเฉพาะหลัก (Main Only)" if not st.session_state.show_prod_only_q else "ขยายดูรายกลุ่ม (Show All)", on_click=toggle_prod_view_q, use_container_width=True, key="btn_prod_q")

    p_map = { "LC": "LC & CK", "CK": "LC & CK", "OM": "OM & JC", "JC": "OM & JC", "OT": "OT/PIGGING", "VP": "OT/PIGGING", "SE": "SE & KW", "KW": "SE & KW" }
    def get_mapped_prod(p): return p_map.get(str(p).strip(), str(p).strip()) if pd.notna(p) else "Unknown"

    prod_q_map = {}
    for row in df_plan_year.itertuples(index=False):
        p = get_mapped_prod(row.Product); g = row.Group if pd.notna(row.Group) else "Others"; v = row.Target; m = row.Month
        if p not in prod_q_map: 
            prod_q_map[p] = {'Q1_P':0, 'Q1_A':0, 'Q2_P':0, 'Q2_A':0, 'Q3_P':0, 'Q3_A':0, 'Q4_P':0, 'Q4_A':0, 'aP':0, 'aA':0, 'groups': {}}
        if g not in prod_q_map[p]['groups']: 
            prod_q_map[p]['groups'][g] = {'Q1_P':0, 'Q1_A':0, 'Q2_P':0, 'Q2_A':0, 'Q3_P':0, 'Q3_A':0, 'Q4_P':0, 'Q4_A':0, 'aP':0, 'aA':0}
        
        q_label = next((q for q, mths in quarters_map.items() if m in mths), None)
        if q_label:
            prod_q_map[p][f'{q_label}_P'] += v
            prod_q_map[p]['groups'][g][f'{q_label}_P'] += v
        prod_q_map[p]['aP'] += v
        prod_q_map[p]['groups'][g]['aP'] += v

    for row in df_so_year.itertuples(index=False):
        p = get_mapped_prod(row.Product); g = row.Group if pd.notna(row.Group) else "Others"; v = row.Actual; m = row.Month
        if p not in prod_q_map: 
            prod_q_map[p] = {'Q1_P':0, 'Q1_A':0, 'Q2_P':0, 'Q2_A':0, 'Q3_P':0, 'Q3_A':0, 'Q4_P':0, 'Q4_A':0, 'aP':0, 'aA':0, 'groups': {}}
        if g not in prod_q_map[p]['groups']: 
            prod_q_map[p]['groups'][g] = {'Q1_P':0, 'Q1_A':0, 'Q2_P':0, 'Q2_A':0, 'Q3_P':0, 'Q3_A':0, 'Q4_P':0, 'Q4_A':0, 'aP':0, 'aA':0}
        
        q_label = next((q for q, mths in quarters_map.items() if m in mths), None)
        if q_label:
            prod_q_map[p][f'{q_label}_A'] += v
            prod_q_map[p]['groups'][g][f'{q_label}_A'] += v
        prod_q_map[p]['aA'] += v
        prod_q_map[p]['groups'][g]['aA'] += v

    hp_parts_q = []
    hp_parts_q.append('<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.05);"><table class="custom-table" style="min-width: 1400px;"><thead><tr><th rowspan="2" style="text-align: left; background-color: white; font-size: 14px; position: sticky; left: 0; z-index: 2;">Product / Group</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q1</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q2</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q3</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0;">Q4</th><th colspan="4" style="font-size: 14px; text-transform: uppercase; text-align: center; border-left: 2px solid #e2e8f0; border-right: none;">Total Year</th></tr><tr style="font-size: 12px;">')
    for i in range(5):
        bl = "border-left: 2px solid #e2e8f0;" if i > 0 else ""
        br = "border-right: none;" if i == 4 else ""
        hp_parts_q.append(f'<th class="text-right" style="{bl}">Plan</th><th class="text-right">Actual</th><th class="text-center">%</th><th class="text-right" style="color: #ef4444; {br}">Need</th>')
    hp_parts_q.append('</tr></thead><tbody>')
    
    gT_prod_q = {f'Q{i}_P': 0 for i in range(1, 5)}; gT_prod_q.update({f'Q{i}_A': 0 for i in range(1, 5)})
    gT_prod_q['aP'] = 0; gT_prod_q['aA'] = 0
    
    sorted_prods_q = sorted(prod_q_map.keys(), key=lambda x: prod_q_map[x]['aP'], reverse=True)

    for prod in sorted_prods_q:
        d = prod_q_map[prod]
        if d['aP'] == 0 and d['aA'] == 0: continue
        for k in gT_prod_q.keys(): gT_prod_q[k] += d[k]
        gT_prod_q['aP'] += d['aP']; gT_prod_q['aA'] += d['aA']
        
        has_sub = len(d['groups']) > 0
        row_html = f'<tr class="group-row bg-slate-200"><td style="border-right: 1px solid #e2e8f0; background-color: #f8fafc; color: #3730a3; font-weight: bold; font-size: 15px; position: sticky; left: 0; z-index: 1;"><span style="display:inline-block; width:12px;"></span>🔹 {prod}</td>'
        row_html += mk_cell_q(d['Q1_P'], d['Q1_A'], True)
        row_html += mk_cell_q(d['Q2_P'], d['Q2_A'], True, True)
        row_html += mk_cell_q(d['Q3_P'], d['Q3_A'], True, True)
        row_html += mk_cell_q(d['Q4_P'], d['Q4_A'], True, True)
        row_html += mk_cell_q(d['aP'], d['aA'], True, True, True, short_num=True)
        row_html += '</tr>'
        hp_parts_q.append(row_html)
        
        if has_sub and not st.session_state.show_prod_only_q:
            sorted_groups = sorted(d['groups'].keys(), key=lambda x: group_order.index(x) if x in group_order else 99)
            for g_name in sorted_groups:
                gD = d['groups'][g_name]
                if gD['aP'] == 0 and gD['aA'] == 0: continue
                r_html = f'<tr><td style="padding-left: 28px; border-right: 1px solid #e2e8f0; font-size: 14px; position: sticky; left: 0; z-index: 1; background-color: white; color: #64748b;">GROUP {g_name}</td>'
                r_html += mk_cell_q(gD['Q1_P'], gD['Q1_A'])
                r_html += mk_cell_q(gD['Q2_P'], gD['Q2_A'], False, True)
                r_html += mk_cell_q(gD['Q3_P'], gD['Q3_A'], False, True)
                r_html += mk_cell_q(gD['Q4_P'], gD['Q4_A'], False, True)
                r_html += mk_cell_q(gD['aP'], gD['aA'], False, True, True, short_num=True)
                r_html += '</tr>'
                hp_parts_q.append(r_html)

    foot_html_prod = f'</tbody><tfoot><tr style="background-color: #e0e7ff; font-weight: bold; color: #312e81;"><td style="border-right: 1px solid #e2e8f0; text-transform: uppercase; font-size: 15px; position: sticky; left: 0; z-index: 1;">Grand Total</td>'
    foot_html_prod += mk_cell_q(gT_prod_q['Q1_P'], gT_prod_q['Q1_A'], True)
    foot_html_prod += mk_cell_q(gT_prod_q['Q2_P'], gT_prod_q['Q2_A'], True, True)
    foot_html_prod += mk_cell_q(gT_prod_q['Q3_P'], gT_prod_q['Q3_A'], True, True)
    foot_html_prod += mk_cell_q(gT_prod_q['Q4_P'], gT_prod_q['Q4_A'], True, True)
    foot_html_prod += mk_cell_q(gT_prod_q['aP'], gT_prod_q['aA'], True, True, True, short_num=True)
    foot_html_prod += '</tr></tfoot></table></div>'
    hp_parts_q.append(foot_html_prod)
    
    st.markdown("".join(hp_parts_q), unsafe_allow_html=True)

with tab3:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); padding: 14px 20px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 12px; font-family: 'Sarabun', sans-serif;">
            <h2 style="color: white; font-size: 20px; margin: 0; font-weight: bold; letter-spacing: 0.5px; font-family: 'Sarabun', sans-serif;">📉 Trend & Breakdown</h2>
            <span style="color: #ccfbf1; font-size: 15px; font-family: 'Sarabun', sans-serif;">| วิเคราะห์แนวโน้มยอดขายและข้อมูลลูกค้ายอดฮิต (Top 10)</span>
        </div>
    """, unsafe_allow_html=True)

    # --------------------------- ตัวกรองพนักงานขาย (เฉพาะ Tab 3) ---------------------------
    t3_col_title, t3_col_filter = st.columns([7.5, 2.5])
    with t3_col_filter:
        all_reps_t3 = sorted(list(df_so_year[df_so_year['SalesRep'] != 'Unknown']['SalesRep'].dropna().unique()))
        selected_rep_t3 = st.selectbox("👤 กรองตามพนักงานขาย:", ["All"] + all_reps_t3, key="t3_rep_filter")
        
    # ตัดข้อมูลตามพนักงานขายที่เลือก
    if selected_rep_t3 == "All":
        t3_df_plan_year = df_plan_year
        t3_df_so_year = df_so_year
    else:
        t3_df_plan_year = df_indiv_year[df_indiv_year['SalesRep'] == selected_rep_t3]
        t3_df_so_year = df_so_year[df_so_year['SalesRep'] == selected_rep_t3]

    with t3_col_title:
        # =========================================================
        # 1. กราฟรายเดือน (ปีที่เลือก) + ตารางข้อมูล
        # =========================================================
        st.markdown(f'<div style="font-size: 15px; color: #1e293b; margin-top: 22px; margin-bottom: 8px; font-weight: bold; text-transform: uppercase; font-family: \'Sarabun\', sans-serif;"><i class="fa-solid fa-chart-column" style="margin-right: 8px; color: #3b82f6;"></i>PLAN & SO และจำนวนลูกค้า ปี {selected_year} (MONTHLY)</div>', unsafe_allow_html=True)
    
    plan_m = t3_df_plan_year.groupby('Month')['Target'].sum().reindex(range(1,13), fill_value=0)
    so_m = t3_df_so_year.groupby('Month')['Actual'].sum().reindex(range(1,13), fill_value=0)
    cust_m = t3_df_so_year.groupby('Month')['Customer'].nunique().reindex(range(1,13), fill_value=0)
    
    merged_m = pd.DataFrame({'Month': range(1, 13), 'Target': plan_m.values, 'Actual': so_m.values, 'CustCount': cust_m.values})
    
    fig_m = go.Figure()
    
    # แท่ง Plan (สีเทาอ่อน/ฟ้าอ่อน ให้เป็นเหมือนพื้นหลังแบคกราวด์)
    fig_m.add_trace(go.Bar(
        x=merged_m['Month'], y=merged_m['Target'], 
        name='Plan/Target (฿)', 
        marker_color='#cbd5e1', 
        marker_line_width=0, 
        yaxis='y1',
        hovertemplate='<b>Plan:</b> %{y:,.0f} ฿<extra></extra>'
    ))
    
    # แท่ง Actual (สีน้ำเงินเข้ม โดดเด่น พร้อมแสดงตัวเลขย่อบนกราฟ)
    fig_m.add_trace(go.Bar(
        x=merged_m['Month'], y=merged_m['Actual'], 
        name='Actual (฿)', 
        marker_color='#4f46e5', 
        marker_line_width=0, 
        yaxis='y1',
        text=merged_m['Actual'].apply(lambda x: format_num_short(x) if x > 0 else ''),
        textposition='outside',
        textfont=dict(size=10, color='#4f46e5', weight='bold'),
        hovertemplate='<b>Actual:</b> %{y:,.0f} ฿<extra></extra>'
    ))
    
    # เส้นลูกค้า (สีส้มอำพัน เส้นโค้งสมูท)
    fig_m.add_trace(go.Scatter(
        x=merged_m['Month'], y=merged_m['CustCount'], 
        name='จำนวนลูกค้า (ราย)', 
        mode='lines+markers', 
        yaxis='y2', 
        line=dict(width=4, shape='spline', color='#f59e0b'), 
        marker=dict(size=10, color='#f59e0b', symbol='circle', line=dict(width=2, color='white')),
        hovertemplate='<b>Customers:</b> %{y} ราย<extra></extra>'
    ))
    
    fig_m.update_layout(
        font=dict(family="'Canva Sans', 'Sarabun', sans-serif", size=12, color='#475569'), 
        barmode='group', 
        bargap=0.2,
        margin=dict(l=10, r=10, t=40, b=20), 
        plot_bgcolor='rgba(255,255,255,1)', 
        paper_bgcolor='rgba(255,255,255,0)',
        hovermode="x unified", # ป๊อปอัปรวมข้อมูลแบบ Infographic
        yaxis=dict(
            title=dict(text="ยอดขาย (บาท)", font=dict(size=11, color='#94a3b8')),
            gridcolor='#f1f5f9', gridwidth=1, zeroline=True, zerolinecolor='#e2e8f0', 
            tickfont=dict(size=11, color='#94a3b8')
        ), 
        yaxis2=dict(
            title=dict(text="จำนวนลูกค้า (ราย)", font=dict(size=11, color='#f59e0b')),
            overlaying='y', side='right', showgrid=False, 
            tickfont=dict(size=11, color='#f59e0b', weight='bold')
        ),
        xaxis=dict(
            tickmode='array', tickvals=list(range(1,13)), 
            ticktext=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 
            tickfont=dict(size=12, weight="bold", color='#334155'), showticklabels=True
        ), 
        height=380,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, 
            font=dict(size=11, color='#475569'),
            bgcolor='rgba(255,255,255,0.9)', bordercolor='#f1f5f9', borderwidth=1
        )
    )
    st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})

    # สร้าง HTML Table แบบแยกออกจากกราฟ
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    tbl_html = '<div style="border: 1px solid #e5e7eb; border-radius: 8px; overflow-x: auto; background: white; margin-top: 16px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);"><table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 15px;">'
    
    # Header Row
    tbl_html += '<tr style="border-bottom: 1px solid #e5e7eb; background-color: #f8fafc;"><th style="padding: 12px; font-weight: bold; color: #475569; text-align: right; border-right: 1px solid #e5e7eb; width: 12%;"></th>'
    for m in month_names:
        tbl_html += f'<th style="padding: 12px; font-weight: bold; color: #475569; border-right: 1px solid #f1f5f9; width: 7.33%;">{m}</th>'
    tbl_html += '</tr>'
    
    # PLAN Row
    tbl_html += '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 12px; font-weight: bold; color: #1e293b; text-align: right; border-right: 1px solid #e5e7eb;">PLAN</td>'
    for i in range(1, 13):
        tbl_html += f'<td style="padding: 12px; color: #334155; border-right: 1px solid #f1f5f9;">{safe_fmt(plan_m.get(i, 0))}</td>'
    tbl_html += '</tr>'
    
    # SO Row
    tbl_html += '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 12px; font-weight: bold; color: #1e293b; text-align: right; border-right: 1px solid #e5e7eb;">SO</td>'
    for i in range(1, 13):
        tbl_html += f'<td style="padding: 12px; color: #4f46e5; border-right: 1px solid #f1f5f9; font-weight: 700;">{safe_fmt(so_m.get(i, 0))}</td>'
    tbl_html += '</tr>'
    
    # % Achieve Row
    tbl_html += '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 12px; font-weight: bold; color: #1e293b; text-align: right; border-right: 1px solid #e5e7eb;">% Achieve</td>'
    for i in range(1, 13):
        p = float(plan_m.get(i, 0))
        a = float(so_m.get(i, 0))
        pct = (a/p*100) if p > 0 else 0
        color = "#dc2626" if pct < 100 else "#16a34a"
        icon = "▼" if pct < 100 else "▲"
        if p == 0 and a == 0: color, icon = "#dc2626", "▼"
        tbl_html += f'<td style="padding: 12px; font-weight: bold; color: {color}; border-right: 1px solid #f1f5f9;">{icon} {pct:.0f}%</td>'
    tbl_html += '</tr>'
    
    # Keep Focust Row
    tbl_html += '<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 12px; font-weight: bold; color: #dc2626; text-align: right; border-right: 1px solid #e5e7eb;">Keep Focus</td>'
    for i in range(1, 13):
        p = float(plan_m.get(i, 0))
        a = float(so_m.get(i, 0))
        foc = p - a if p > a else 0
        tbl_html += f'<td style="padding: 12px; font-weight: bold; color: #dc2626; border-right: 1px solid #f1f5f9;">{safe_fmt(foc)}</td>'
    tbl_html += '</tr>'

    # Customers Row
    tbl_html += '<tr><td style="padding: 12px; font-weight: bold; color: #f59e0b; text-align: right; border-right: 1px solid #e5e7eb;"># Customers</td>'
    for i in range(1, 13):
        tbl_html += f'<td style="padding: 12px; font-weight: bold; color: #f59e0b; border-right: 1px solid #f1f5f9;">{int(cust_m.get(i, 0))}</td>'
    tbl_html += '</tr>'

    tbl_html += '</table></div>'
    
    st.markdown(tbl_html, unsafe_allow_html=True)


    # =========================================================
    # 2. กราฟย้อนหลัง 10 ปี
    # =========================================================
    st.markdown(f'<div style="font-size: 15px; color: #1e293b; margin-bottom: 8px; font-weight: bold; text-transform: uppercase;"><i class="fa-solid fa-chart-line" style="margin-right: 8px; color: #10b981;"></i>PLAN & SO และจำนวนลูกค้า ย้อนหลัง 10 ปี (10-YEAR HISTORICAL TREND)</div>', unsafe_allow_html=True)
    
    # คำนวณข้อมูล 10 ปี (นำ Filter พนักงานขายมาใช้ด้วย)
    df_plan_10y = df_plan_all if selected_group == "All" else df_plan_all[df_plan_all['Group'] == selected_group].copy()
    df_so_10y = df_so_all if selected_group == "All" else df_so_all[df_so_all['Group'] == selected_group].copy()

    if selected_rep_t3 != "All":
        df_plan_10y = df_indiv_all if selected_group == "All" else df_indiv_all[df_indiv_all['Group'] == selected_group].copy()
        df_plan_10y = df_plan_10y[df_plan_10y['SalesRep'] == selected_rep_t3]
        df_so_10y = df_so_10y[df_so_10y['SalesRep'] == selected_rep_t3]

    df_plan_10y['YearInt'] = pd.to_numeric(df_plan_10y['Year'], errors='coerce')
    df_so_10y['YearInt'] = pd.to_numeric(df_so_10y['Year'], errors='coerce')

    all_years = sorted(list(set(df_plan_10y['YearInt'].dropna().unique()) | set(df_so_10y['YearInt'].dropna().unique())), reverse=True)[:10]
    all_years = sorted([int(y) for y in all_years]) # เรียงจากน้อยไปมากสำหรับกราฟ

    plan_10y_agg = df_plan_10y[df_plan_10y['YearInt'].isin(all_years)].groupby('YearInt')['Target'].sum().reset_index()
    so_10y_agg = df_so_10y[df_so_10y['YearInt'].isin(all_years)].groupby('YearInt')['Actual'].sum().reset_index()
    cust_10y_agg = df_so_10y[df_so_10y['YearInt'].isin(all_years)].groupby('YearInt')['Customer'].nunique().reset_index()

    merged_10y = pd.DataFrame({'YearInt': all_years}).merge(plan_10y_agg, on='YearInt', how='left').merge(so_10y_agg, on='YearInt', how='left').merge(cust_10y_agg, on='YearInt', how='left').fillna(0)
    
    fig_10y = go.Figure()
    
    fig_10y.add_trace(go.Bar(
        x=merged_10y['YearInt'].astype(str), y=merged_10y['Target'], 
        name='Plan/Target (฿)', 
        marker_color='#cbd5e1', 
        marker_line_width=0, 
        yaxis='y1',
        hovertemplate='<b>Plan:</b> %{y:,.0f} ฿<extra></extra>'
    ))
    
    fig_10y.add_trace(go.Bar(
        x=merged_10y['YearInt'].astype(str), y=merged_10y['Actual'], 
        name='Actual (฿)', 
        marker_color='#4f46e5', 
        marker_line_width=0, 
        yaxis='y1',
        text=merged_10y['Actual'].apply(lambda x: format_num_short(x) if x > 0 else ''),
        textposition='outside',
        textfont=dict(size=10, color='#4f46e5', weight='bold'),
        hovertemplate='<b>Actual:</b> %{y:,.0f} ฿<extra></extra>'
    ))
    
    fig_10y.add_trace(go.Scatter(
        x=merged_10y['YearInt'].astype(str), y=merged_10y['Customer'], 
        name='จำนวนลูกค้า (ราย)', 
        mode='lines+markers', 
        yaxis='y2', 
        line=dict(width=4, shape='spline', color='#f59e0b'), 
        marker=dict(size=10, color='#f59e0b', symbol='circle', line=dict(width=2, color='white')),
        hovertemplate='<b>Customers:</b> %{y} ราย<extra></extra>'
    ))
    
    fig_10y.update_layout(
        font=dict(family="'Canva Sans', 'Sarabun', sans-serif", size=12, color='#475569'), 
        barmode='group', 
        bargap=0.2,
        margin=dict(l=10, r=10, t=40, b=20), 
        plot_bgcolor='rgba(255,255,255,1)', 
        paper_bgcolor='rgba(255,255,255,0)',
        hovermode="x unified",
        yaxis=dict(
            title=dict(text="ยอดขาย (บาท)", font=dict(size=11, color='#94a3b8')),
            gridcolor='#f1f5f9', gridwidth=1, zeroline=True, zerolinecolor='#e2e8f0', 
            tickfont=dict(size=11, color='#94a3b8')
        ), 
        yaxis2=dict(
            title=dict(text="จำนวนลูกค้า (ราย)", font=dict(size=11, color='#f59e0b')),
            overlaying='y', side='right', showgrid=False, 
            tickfont=dict(size=11, color='#f59e0b', weight='bold')
        ),
        xaxis=dict(
            type='category', # 🔥 เพิ่มคำสั่งนี้เพื่อบังคับให้กราฟมองปีเป็น "ข้อความหมวดหมู่" ไม่ใช่ตัวเลขต่อเนื่อง
            tickfont=dict(size=12, weight="bold", color='#334155')
        ),
        height=380,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, 
            font=dict(size=11, color='#475569'),
            bgcolor='rgba(255,255,255,0.9)', bordercolor='#f1f5f9', borderwidth=1
        )
    )
    st.plotly_chart(fig_10y, use_container_width=True, config={'displayModeBar': False})


    # =========================================================
    # 3. TOP 10 CUSTOMERS & INDUSTRIES
    # =========================================================
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size: 18px; color: #1e3a8a; margin-bottom: 20px; font-weight: bold; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">🌟 TOP 10 CUSTOMERS & INDUSTRIES</div>', unsafe_allow_html=True)

    def build_top10_html(df, title, icon, col1_name, col2_name, col3_name=None, col4_name=None):
        html = f'<div style="margin-bottom: 0;"><div style="font-size: 14px; color: #475569; margin-bottom: 8px; font-weight: 600; text-transform: uppercase;">{icon} {title}</div><table style="width: 100%; border-collapse: collapse; border: 1px solid #e2e8f0; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); font-size: 13px;">'
        
        th3 = f'<th style="padding: 10px 8px; border-right: 1px solid #e2e8f0; text-align: center;">{col3_name}</th>' if col3_name else ''
        th4 = f'<th style="padding: 10px 8px; border-right: 1px solid #e2e8f0; text-align: center;">{col4_name}</th>' if col4_name else ''
        
        html += f'<thead style="background-color: #f8fafc; color: #64748b; text-transform: uppercase; font-size: 11px;"><tr><th style="padding: 10px 8px; border-right: 1px solid #e2e8f0; text-align: left;">{col1_name}</th>{th3}{th4}<th style="padding: 10px 8px; text-align: right;">{col2_name}</th></tr></thead><tbody style="background-color: white;">'
        for _, row in df.iterrows():
            name = escape_html(str(row.iloc[0]))
            val2 = str(row.iloc[1])
            
            td3 = ''
            if col3_name:
                val3 = str(row.iloc[2])
                color_v3 = "#f59e0b" if col3_name == "Customers" else "#0ea5e9" # ใช้สีฟ้าสำหรับวันที่ และสีส้มสำหรับจำนวนคน
                td3 = f'<td style="padding: 8px; text-align: center; color: {color_v3}; border-right: 1px solid #f1f5f9; font-weight: bold; font-size: 12px;">{val3}</td>'
                
            td4 = ''
            if col4_name:
                val4 = str(row.iloc[3])
                td4 = f'<td style="padding: 8px; text-align: center; color: #10b981; border-right: 1px solid #f1f5f9; font-weight: bold; font-size: 11px; max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{escape_html(val4)}">{escape_html(val4)}</td>'
                
            # แก้ไข: ให้ชื่อลูกค้าแสดงแบบเต็มๆ ปลด max-width, ellipsis และ white-space: nowrap ออก
            html += f'<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; color: #334155; border-right: 1px solid #f1f5f9;"><div style="word-wrap: break-word; white-space: normal;" title="{name}">{name}</div></td>{td3}{td4}<td style="padding: 8px; text-align: right; color: #4338ca; font-weight: bold;">{val2}</td></tr>'
        for _ in range(10 - len(df)):
            td3_empty = '<td style="padding: 8px; text-align: center; color: #cbd5e1; border-right: 1px solid #f1f5f9;">-</td>' if col3_name else ''
            td4_empty = '<td style="padding: 8px; text-align: center; color: #cbd5e1; border-right: 1px solid #f1f5f9;">-</td>' if col4_name else ''
            html += f'<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 8px; color: #cbd5e1; border-right: 1px solid #f1f5f9; height: 35px;">-</td>{td3_empty}{td4_empty}<td style="padding: 8px; text-align: right; color: #cbd5e1;">-</td></tr>'
        html += '</tbody></table></div>'
        return html

    # ข้อมูลปีที่เลือก (แสดงข้อมูลทั้งปี ไม่ต้องกรองตามเดือนที่เลือก)
    df_top_cust_yr = t3_df_so_year.groupby('Customer').agg(
        Actual=('Actual', 'sum'),
        LastDate=('SODate', 'max'),
        Industry=('Industry', 'first')
    ).reset_index().sort_values('Actual', ascending=False).head(10)
    df_top_cust_yr['Actual'] = df_top_cust_yr['Actual'].apply(lambda x: safe_fmt(x))
    df_top_cust_yr['LastDate'] = df_top_cust_yr['LastDate'].apply(lambda x: format_th_date(x) if pd.notna(x) else '-')
    
    # ดึงข้อมูล Top 10 อุตสาหกรรม พร้อมนับจำนวนลูกค้าแบบไม่ซ้ำ
    df_top_ind_yr = t3_df_so_year.groupby('Industry').agg(
        Actual=('Actual', 'sum'),
        CustCount=('Customer', 'nunique')
    ).reset_index().sort_values('Actual', ascending=False).head(10)
    df_top_ind_yr['Actual'] = df_top_ind_yr['Actual'].apply(lambda x: safe_fmt(x))

    # ข้อมูล 10 ปี
    df_so_10y_filtered = df_so_10y[df_so_10y['YearInt'].isin(all_years)]
    
    df_top_cust_10y = df_so_10y_filtered.groupby('Customer').agg(
        Actual=('Actual', 'sum'),
        LastDate=('SODate', 'max'),
        Industry=('Industry', 'first')
    ).reset_index().sort_values('Actual', ascending=False).head(10)
    df_top_cust_10y['Actual'] = df_top_cust_10y['Actual'].apply(lambda x: safe_fmt(x))
    df_top_cust_10y['LastDate'] = df_top_cust_10y['LastDate'].apply(lambda x: format_th_date(x) if pd.notna(x) else '-')
    
    # ดึงข้อมูล Top 10 อุตสาหกรรม (ย้อนหลัง 10 ปี) พร้อมนับจำนวนลูกค้าแบบไม่ซ้ำ
    df_top_ind_10y = df_so_10y_filtered.groupby('Industry').agg(
        Actual=('Actual', 'sum'),
        CustCount=('Customer', 'nunique')
    ).reset_index().sort_values('Actual', ascending=False).head(10)
    df_top_ind_10y['Actual'] = df_top_ind_10y['Actual'].apply(lambda x: safe_fmt(x))

    # แสดงผลแบ่ง 2 แถว
    st.markdown(f'<div style="font-size: 15px; color: #0284c7; margin-bottom: 12px; font-weight: bold; background-color: #f0f9ff; padding: 8px 12px; border-left: 4px solid #0ea5e9; border-radius: 4px;">📅 ข้อมูลรวมทั้งปี {selected_year}</div>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1: st.markdown(build_top10_html(df_top_cust_yr, "TOP 10 CUSTOMERS", "🏆", "Customer", "Actual (฿)", "Last PO", "INDS"), unsafe_allow_html=True)
    with t2: st.markdown(build_top10_html(df_top_ind_yr, "TOP 10 INDUSTRIES", "🏭", "Industry", "Actual (฿)", "Customers"), unsafe_allow_html=True)

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    
    st.markdown(f'<div style="font-size: 15px; color: #16a34a; margin-bottom: 12px; font-weight: bold; background-color: #f0fdf4; padding: 8px 12px; border-left: 4px solid #22c55e; border-radius: 4px;">🕰️ ข้อมูลสะสมย้อนหลัง 10 ปี (รวมทุกเดือน)</div>', unsafe_allow_html=True)
    t3, t4 = st.columns(2)
    with t3: st.markdown(build_top10_html(df_top_cust_10y, "TOP 10 CUSTOMERS (10 YEARS)", "🏆", "Customer", "Actual (฿)", "Last PO", "INDS"), unsafe_allow_html=True)
    with t4: st.markdown(build_top10_html(df_top_ind_10y, "TOP 10 INDUSTRIES (10 YEARS)", "🏭", "Industry", "Actual (฿)", "Customers"), unsafe_allow_html=True)

with tab4:
    st.markdown("""
        <style>
            /* ปรับแต่งปุ่ม Radio (Plan Sales / Plan Account) ให้ขยายเท่ากันและคุมโทนสีเขียวอมฟ้า */
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] {
                width: 100% !important;
            }
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label {
                flex: 1 1 50% !important;
                width: 50% !important;
                padding: 10px 12px !important;
                border: 1px solid #99f6e4 !important;
            }
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label:hover {
                background-color: #f0fdfa !important;
                border-color: #0d9488 !important;
            }
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label:has(input:checked),
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[data-checked="true"],
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[aria-checked="true"] {
                background-color: #0d9488 !important;
                border-color: #0d9488 !important;
                box-shadow: 0 2px 4px rgba(13, 148, 136, 0.2) !important;
            }
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label:has(input:checked) p,
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[data-checked="true"] p,
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label[aria-checked="true"] p {
                color: white !important;
            }
            [data-testid="stMainBlockContainer"] div[role="radiogroup"] > label p {
                font-family: 'Sarabun', sans-serif !important;
                font-size: 15px !important;
                color: #0f766e !important;
            }
        </style>
        <div style="border-left: 4px solid #0d9488; background-color: #f0fdfa; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); display: flex; align-items: center; flex-wrap: wrap; gap: 8px; font-family: 'Sarabun', sans-serif;">
            <h2 style="color: #115e59; font-size: 18px; margin: 0; font-family: 'Sarabun', sans-serif;">🧾 สรุปผลงานเปิดอินวอยซ์ (Invoice Performance)</h2>
            <span style="color: #0f766e; font-size: 15px; font-family: 'Sarabun', sans-serif;">| เปรียบเทียบผลรวมมูลค่างาน อินวอยซ์ จำนวนงาน และกำไร เทียบกับเป้าหมาย KPI</span>
            <div style="width: 100%; color: #ef4444; font-size: 14px; font-weight: bold; font-style: italic; margin-top: 2px;">*** ตัวเลขอย่างไม่เป็นทางการ ***</div>
        </div>
    """, unsafe_allow_html=True)
    
    if 'inv_target' not in st.session_state: st.session_state.inv_target = 'Plan Sales'
    target_col = 'PlanSales' if st.session_state.inv_target == 'Plan Sales' else 'PlanAcc'
    target_name = st.session_state.inv_target
    
    def metric_card_inv(col, subtitle, plan, actual, profit, invoices, so_count):
        achieve = (actual / plan * 100) if plan > 0 else 0
        margin_pct = (profit / actual * 100) if actual > 0 else 0
        gap = actual - plan
        gap_color = "#00b862" if gap >= 0 else "#dc2626"
        gap_sign = "+" if gap > 0 else ""
        
        html = f"""
        <div style="background-color: white; border: 1px solid #5eead4; border-radius: 8px; padding: 24px 16px; box-shadow: 0 2px 6px rgba(13, 148, 136, 0.05); font-family: 'Arimo', 'Canva Sans', 'Sarabun', sans-serif;">
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="background-color: #ccfbf1; color: #0f766e; padding: 6px 16px; border-radius: 6px; font-size: 14px; font-weight: 700;">{subtitle}</span>
            </div>
            <div style="text-align: center; padding-bottom: 20px; border-bottom: 1px solid #99f6e4; margin-bottom: 20px;">
                <div style="font-size: 32px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(plan)}</div>
                <div style="font-size: 14px; color: #6b7280; font-style: italic; margin-top: 4px;">Plan ({target_name})</div>
            </div>
            <div style="display: flex; text-align: center;">
                <div style="flex: 1.1; border-right: 1px solid #99f6e4; padding: 0 4px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 26px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(actual)}</div>
                        <div style="font-size: 13px; color: #6b7280; font-style: italic;">InvActual</div>
                    </div>
                    <div style="display: flex; justify-content: space-around;">
                        <div>
                            <div style="font-size: 22px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(invoices)}</div>
                            <div style="font-size: 13px; color: #6b7280; font-style: italic;">Invoices</div>
                        </div>
                        <div>
                            <div style="font-size: 22px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(so_count)}</div>
                            <div style="font-size: 13px; color: #6b7280; font-style: italic;">SO Count:</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 0.9; border-right: 1px solid #99f6e4; padding: 0 4px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 26px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(achieve, 1)}%</div>
                        <div style="font-size: 13px; color: #6b7280; font-style: italic;">Achievement</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(margin_pct, 1)}%</div>
                        <div style="font-size: 13px; color: #6b7280; font-style: italic;">Margin</div>
                    </div>
                </div>
                <div style="flex: 1; padding: 0 4px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="margin-bottom: 20px;">
                        <div style="font-size: 26px; font-weight: 800; color: {gap_color}; line-height: 1.2;">{gap_sign}{safe_fmt(gap)}</div>
                        <div style="font-size: 13px; color: {gap_color}; font-style: italic;">Keep Focus</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: 800; color: #000; line-height: 1.2;">{safe_fmt(profit)}</div>
                        <div style="font-size: 13px; color: #6b7280; font-style: italic;">Profit</div>
                    </div>
                </div>
            </div>
        </div>
        """
        col.markdown(html, unsafe_allow_html=True)
        
    # 1. ข้อมูลรายเดือน (Period)
    i_plan_period = df_invplan_year[df_invplan_year['Month'].isin(selected_month)][target_col].sum()
    df_inv_period = df_inv_year[df_inv_year['Month'].isin(selected_month)]
    i_act_period = df_inv_period['Value'].sum()
    i_prof_period = df_inv_period['Profit'].sum()
    i_inv_period = df_inv_period['InvNo'].nunique()
    i_so_period = df_inv_period['RefSoNumber'].nunique()

    # 2. ข้อมูลยอดสะสม (YTD)
    i_plan_ytd = df_invplan_year[df_invplan_year['Month'] <= max_m][target_col].sum()
    df_inv_ytd = df_inv_year[df_inv_year['Month'] <= max_m]
    i_act_ytd = df_inv_ytd['Value'].sum()
    i_prof_ytd = df_inv_ytd['Profit'].sum()
    i_inv_ytd = df_inv_ytd['InvNo'].nunique()
    i_so_ytd = df_inv_ytd['RefSoNumber'].nunique()

    # 3. ข้อมูลยอดรวมทั้งปี (Annual)
    i_plan_ann = df_invplan_year[target_col].sum()
    i_act_ann = df_inv_year['Value'].sum()
    i_prof_ann = df_inv_year['Profit'].sum()
    i_inv_ann = df_inv_year['InvNo'].nunique()
    i_so_ann = df_inv_year['RefSoNumber'].nunique()

    c1, c2, c3 = st.columns(3)
    metric_card_inv(c1, sub_period, i_plan_period, i_act_period, i_prof_period, i_inv_period, i_so_period)
    metric_card_inv(c2, sub_ytd, i_plan_ytd, i_act_ytd, i_prof_ytd, i_inv_ytd, i_so_ytd)
    metric_card_inv(c3, sub_annual, i_plan_ann, i_act_ann, i_prof_ann, i_inv_ann, i_so_ann)
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    head_col, btn_col = st.columns([4.5, 5.5])
    with head_col: st.markdown('<h3 style="color: #0f766e; font-size: 18px; margin-bottom: 0; padding-top: 10px; font-family: \'Sarabun\', sans-serif;">📊 ตารางเปรียบเทียบเป้าหมาย KPI vs ยอดอินวอยซ์จริง (Group Level)</h3>', unsafe_allow_html=True)
    with btn_col:
        bc1, bc2 = st.columns([6, 4])
        with bc1:
            st.radio("เลือกเป้าหมาย:", ['Plan Sales', 'Plan Account'], key='inv_target', horizontal=True, label_visibility="collapsed")
        with bc2:
            if 'expand_inv_groups' not in st.session_state: st.session_state.expand_inv_groups = True
            def toggle_inv_groups(): st.session_state.expand_inv_groups = not st.session_state.expand_inv_groups
            st.button("ย่อดูเฉพาะเดือน" if st.session_state.expand_inv_groups else "ขยายดูทุกกลุ่ม", on_click=toggle_inv_groups, use_container_width=True)

    inv_parts = []
    inv_parts.append('<div style="border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); background-color: white;"><table class="custom-table" style="white-space: nowrap; width: 100%; border-collapse: collapse;">')
    
    # --- TABLE HEADER ---
    inv_parts.append(f'''
    <thead style="font-family: 'Sarabun', sans-serif;">
        <tr>
            <th rowspan="2" style="background-color: #f8fafc; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; vertical-align: middle; text-align: left; padding: 12px 16px;">
                <div style="font-size: 13px; color: #475569; font-weight: bold; margin-bottom: 4px;">ปี {selected_year}</div>
                <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">MONTH / GROUP</div>
            </th>
            <th colspan="5" style="background-color: #f8fafc; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; text-align: center; padding: 10px; font-size: 13px; color: #475569;">{hdr_period}</th>
            <th colspan="5" style="background-color: #f8fafc; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; text-align: center; padding: 10px; font-size: 13px; color: #475569;">{hdr_ytd}</th>
            <th colspan="5" style="background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; text-align: center; padding: 10px; font-size: 13px; color: #475569;">{hdr_year}</th>
        </tr>
        <tr>
    ''')
    for i in range(3):
        br = "border-right: 1px solid #e2e8f0;" if i < 2 else ""
        inv_parts.append(f'''
            <th style="background-color: #ffffff; border-left: 1px solid #f1f5f9; border-bottom: 1px solid #e2e8f0; text-align: center; padding: 8px 6px; font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase;">Jobs</th>
            <th style="background-color: #ffffff; border-bottom: 1px solid #e2e8f0; text-align: right; padding: 8px 6px; font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase;">Actual Inv.</th>
            <th style="background-color: #ffffff; border-bottom: 1px solid #e2e8f0; text-align: right; padding: 8px 6px; font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase;">Profit</th>
            <th style="background-color: #ffffff; border-bottom: 1px solid #e2e8f0; text-align: right; padding: 8px 6px; font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase;">{target_name}</th>
            <th style="background-color: #ffffff; border-bottom: 1px solid #e2e8f0; {br} text-align: center; padding: 8px 6px; font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase;">% Ach.</th>
        ''')
    inv_parts.append('</tr></thead><tbody style="font-size: 14px; font-family: \'Sarabun\', sans-serif;">')

    def mk_inv_cell(jobs, act_val, prof, plan_val, row_type="normal"):
        mg = safe_pct(prof, act_val)
        ach = safe_pct(act_val, plan_val)
        ach_val = (act_val / plan_val * 100) if plan_val > 0 else 0
        
        # UX/UI Theming based on row type
        if row_type == "footer":
            bg = "background-color: #312e81;" # Dark Indigo
            c_job = "color: #ffffff;"
            c_act = "color: #ffffff;"
            c_prof = "color: #6ee7b7;" # Light Teal
            c_mg = "color: #94a3b8;"
            c_plan = "color: #fde047;" # Yellow
            c_ach = "#a7f3d0" if ach_val >= 100 else "#fca5a5"
            b_color = "#4338ca"
            fw = "font-weight: bold;"
            pad = "padding: 12px 8px;"
        elif row_type == "month":
            bg = "background-color: #f8fafc;" # Light slate/blue
            c_job = "color: #64748b;"
            c_act = "color: #312e81;"
            c_prof = "color: #0f766e;"
            c_mg = "color: #94a3b8;"
            c_plan = "color: #334155;"
            c_ach = "#16a34a" if ach_val >= 100 else "#ef4444"
            b_color = "#e2e8f0"
            fw = "font-weight: bold;"
            pad = "padding: 10px 8px;"
        else:
            bg = "background-color: #ffffff;"
            c_job = "color: #475569;"
            c_act = "color: #4338ca;" # Indigo
            c_prof = "color: #0d9488;" # Teal
            c_mg = "color: #cbd5e1;"
            c_plan = "color: #475569;"
            c_ach = "#10b981" if ach_val >= 100 else "#ef4444"
            b_color = "#f1f5f9"
            fw = "font-weight: 600;"
            pad = "padding: 10px 8px;"

        # Status Icons (Green Checkbox / Red Arrow)
        icon = ""
        if plan_val > 0:
            if ach_val >= 100:
                icon_bg = "#22c55e" if row_type != "footer" else "#10b981"
                icon = f' <span style="display:inline-block; background-color:{icon_bg}; color:white; border-radius:3px; padding:0px 4px; font-size:10px; margin-left:4px; vertical-align: middle; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">✓</span>'
            else:
                icon = f' <span style="color:{c_ach}; font-size:10px; margin-left:4px; vertical-align: middle;">▼</span>'

        return f'''
        <td style="{bg} border-left: 1px solid {b_color}; text-align: center; {fw} {c_job} {pad}">{jobs}</td>
        <td style="{bg} text-align: right; {fw} {c_act} {pad}">{safe_fmt(act_val)}</td>
        <td style="{bg} text-align: right; {fw} {c_prof} {pad}">{safe_fmt(prof)} <span style="font-size: 11px; font-weight: normal; {c_mg}">({mg})</span></td>
        <td style="{bg} text-align: right; {fw} {c_plan} {pad}">{safe_fmt(plan_val)}</td>
        <td style="{bg} text-align: center; {fw} color: {c_ach}; border-right: 1px solid {b_color}; {pad}">{ach}{icon}</td>
        '''

    gt = {'p':{'val':0,'prof':0,'jobs':set(),'plan':0}, 'y':{'val':0,'prof':0,'jobs':set(),'plan':0}, 'a':{'val':0,'prof':0,'jobs':set(),'plan':0}}
    arrow_state = '▲' if st.session_state.expand_inv_groups else '▼'
    display_state = 'table-row' if st.session_state.expand_inv_groups else 'none'

    for m in selected_month:
        i_m = df_inv_year[df_inv_year['Month'] == m]; ip_m = df_invplan_year[df_invplan_year['Month'] == m]
        i_y = df_inv_year[df_inv_year['Month'] <= m]; ip_y = df_invplan_year[df_invplan_year['Month'] <= m]
        if i_m.empty and ip_m.empty and i_y.empty and i_y.empty: continue
        mt = {
            'p': {'val': i_m['Value'].sum(), 'prof': i_m['Profit'].sum(), 'jobs': i_m['InvNo'].nunique(), 'plan': ip_m[target_col].sum()},
            'y': {'val': i_y['Value'].sum(), 'prof': i_y['Profit'].sum(), 'jobs': i_y['InvNo'].nunique(), 'plan': ip_y[target_col].sum()},
            'a': {'val': df_inv_year['Value'].sum(), 'prof': df_inv_year['Profit'].sum(), 'jobs': df_inv_year['InvNo'].nunique(), 'plan': df_invplan_year[target_col].sum()}
        }
        
        gt['p']['val'] += mt['p']['val']; gt['p']['prof'] += mt['p']['prof']; gt['p']['plan'] += mt['p']['plan']
        for j in i_m['InvNo'].unique(): gt['p']['jobs'].add(j)
            
        if m == max_m:
            gt['y']['val'] = mt['y']['val']; gt['y']['prof'] = mt['y']['prof']; gt['y']['plan'] = mt['y']['plan']
            for j in i_y['InvNo'].unique(): gt['y']['jobs'].add(j)
            gt['a']['val'] = mt['a']['val']; gt['a']['prof'] = mt['a']['prof']; gt['a']['plan'] = mt['a']['plan']
            for j in df_inv_year['InvNo'].unique(): gt['a']['jobs'].add(j)

        # Month Row
        inv_parts.append(f'<tr style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; cursor: pointer; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#eef2ff\'" onmouseout="this.style.backgroundColor=\'#f8fafc\'" onclick="toggleGroup(\'inv-m-{m}\', this)">')
        inv_parts.append(f'<td style="padding: 10px 16px; border-right: 1px solid #e2e8f0; font-weight: bold; color: #312e81; font-size: 14px;"><span class="arrow-icon" style="display:inline-block; width:16px; color: #6366f1;">{arrow_state}</span> 📅 เดือน{TH_MONTHS[m]}</td>')
        inv_parts.append(mk_inv_cell(mt['p']['jobs'], mt['p']['val'], mt['p']['prof'], mt['p']['plan'], row_type="month"))
        inv_parts.append(mk_inv_cell(mt['y']['jobs'], mt['y']['val'], mt['y']['prof'], mt['y']['plan'], row_type="month"))
        inv_parts.append(mk_inv_cell(mt['a']['jobs'], mt['a']['val'], mt['a']['prof'], mt['a']['plan'], row_type="month"))
        inv_parts.append('</tr>')

        if st.session_state.expand_inv_groups:
            group_order = ['A', 'B', 'C', 'D', 'R', 'COM', 'PD', 'Others']
            for g in group_order:
                g_im = i_m[i_m['Group'] == g]; g_ipm = ip_m[ip_m['Group'] == g]
                g_iy = i_y[i_y['Group'] == g]; g_ipy = ip_y[ip_y['Group'] == g]
                g_ia = df_inv_year[df_inv_year['Group'] == g]; g_ipa = df_invplan_year[df_invplan_year['Group'] == g]
                
                p_val = g_im['Value'].sum(); p_plan = g_ipm[target_col].sum()
                if p_val == 0 and p_plan == 0 and g_iy['Value'].sum() == 0 and g_ipy[target_col].sum() == 0: 
                    continue
                    
                # Normal Group Row
                inv_parts.append(f'<tr class="inv-m-{m}" style="display: {display_state}; border-bottom: 1px solid #f1f5f9; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#f8fafc\'" onmouseout="this.style.backgroundColor=\'white\'">')
                inv_parts.append(f'<td style="padding: 10px 8px 10px 32px; border-right: 1px solid #e2e8f0; font-weight: 500; color: #475569; font-size: 13px;">GROUP {g}</td>')
                inv_parts.append(mk_inv_cell(g_im['InvNo'].nunique(), p_val, g_im['Profit'].sum(), p_plan, row_type="normal"))
                inv_parts.append(mk_inv_cell(g_iy['InvNo'].nunique(), g_iy['Value'].sum(), g_iy['Profit'].sum(), g_ipy[target_col].sum(), row_type="normal"))
                inv_parts.append(mk_inv_cell(g_ia['InvNo'].nunique(), g_ia['Value'].sum(), g_ia['Profit'].sum(), g_ipa[target_col].sum(), row_type="normal"))
                inv_parts.append('</tr>')

    inv_parts.append('</tbody>')
    
    # Grand Total Row
    if gt['a']['val'] > 0 or gt['a']['plan'] > 0:
        inv_parts.append('<tfoot style="background-color: #312e81; color: white; font-weight: bold; font-size: 14px;"><tr>')
        inv_parts.append('<td style="padding: 12px 16px; border-right: 1px solid #4338ca; text-transform: uppercase;">GRAND TOTAL</td>')
        inv_parts.append(mk_inv_cell(len(gt['p']['jobs']), gt['p']['val'], gt['p']['prof'], gt['p']['plan'], row_type="footer"))
        inv_parts.append(mk_inv_cell(len(gt['y']['jobs']), gt['y']['val'], gt['y']['prof'], gt['y']['plan'], row_type="footer"))
        inv_parts.append(mk_inv_cell(len(gt['a']['jobs']), gt['a']['val'], gt['a']['prof'], gt['a']['plan'], row_type="footer"))
        inv_parts.append('</tr></tfoot>')
        
    inv_parts.append('</table></div>')
    components.html(f"{COMMON_HTML_HEAD}<body>{''.join(inv_parts)}</body>", height=600, scrolling=True)

with tab5:
    st.markdown("""
        <style>
            /* บังคับใช้ฟอนต์ Sarabun ใน Tab 5 */
            .tab5-scope, .tab5-scope * { font-family: 'Sarabun', sans-serif !important; }
        </style>
        <div class="tab5-scope" style="border-left: 4px solid #3b82f6; background-color: #eff6ff; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="color: #1e3a8a; font-size: 18px; margin: 0;">🚚 แผนจัดส่งสินค้า (Delivery Schedule)</h2>
            <span style="color: #1d4ed8; font-size: 15px;">| คาดการณ์ปริมาณงานจัดส่ง พร้อมติดตามสถานะการเปิดอินวอยซ์ของแต่ละโครงการ</span>
        </div>
    """, unsafe_allow_html=True)
    
    # คำนวณข้อมูล Delivery
    del_records = []
    month_data = {} 
    
    # 🔥 แยกเก็บข้อมูลสำหรับกราฟ 12 เดือน (ไม่สนใจตัวกรองเดือน)
    chart_month_data = {m: {'val': 0, 'profit': 0} for m in range(1, 13)}

    for so in df_so_all.itertuples(index=False):
        if selected_group != "All" and so.Group != selected_group: continue
        
        so_num = so.SONumber
        del_date_str = soi_del_map.get(so_num, None)
        if not del_date_str or str(del_date_str) == 'nan' or del_date_str == '-': continue
        
        try:
            d_date = pd.to_datetime(del_date_str, format='mixed', dayfirst=True, errors='coerce')
            if pd.isna(d_date): continue
        except:
            continue
            
        d_year = str(d_date.year)
        d_month = d_date.month
        
        if selected_year != 'All' and d_year != selected_year: continue
        
        # 1. บันทึกข้อมูลเข้ากราฟเสมอ (ตราบใดที่อยู่ในปีและกลุ่มที่เลือก)
        if 1 <= d_month <= 12:
            chart_month_data[d_month]['val'] += so.Actual
            chart_month_data[d_month]['profit'] += so.Margin
            
        # 2. คัดกรองด้วยเดือน สำหรับกล่องตัวเลขและตารางรายละเอียด
        if d_month not in selected_month: continue
        
        inv_info = inv_lookup.get(so_num, {'invNos': '', 'invTotalVal': 0})
        
        del_records.append({
            'DelDateObj': d_date,
            'DelDateStr': format_exact_th_date(d_date),
            'Month': d_month,
            'Group': so.Group if pd.notna(so.Group) else 'Others',
            'SalesRep': so.SalesRep,
            'SONumber': so_num,
            'Customer': so.Customer,
            'Product': so.Product,
            'Value': so.Actual,
            'Profit': so.Margin,
            'InvNos': inv_info['invNos'],
            'InvTotalVal': inv_info['invTotalVal']
        })
        
        if d_month not in month_data:
            month_data[d_month] = {'val': 0, 'profit': 0, 'count': 0, 'jobs': [], 'custs': set(), 'pending_inv': 0}
        month_data[d_month]['val'] += so.Actual
        month_data[d_month]['profit'] += so.Margin
        month_data[d_month]['count'] += 1
        month_data[d_month]['jobs'].append(del_records[-1])
        month_data[d_month]['custs'].add(so.Customer)
        
        # เช็คว่ามีรายการที่รอเปิดบิล หรือเปิดบิลแบบบางส่วน (ยังไม่ครบ 98%) หรือไม่
        if not inv_info['invNos'] or inv_info['invTotalVal'] < (so.Actual * 0.98):
            month_data[d_month]['pending_inv'] += 1
        
    df_del = pd.DataFrame(del_records)
    
    tot_del_jobs = len(df_del)
    tot_del_val = df_del['Value'].sum() if not df_del.empty else 0
    tot_del_prof = df_del['Profit'].sum() if not df_del.empty else 0
    tot_del_custs = df_del['Customer'].nunique() if not df_del.empty else 0
    # นับรวมรายการที่ยังไม่มี Invoice หรือยอด Invoice ยังไม่ครบ
    tot_pending_inv = sum(1 for r in del_records if not r['InvNos'] or r['InvTotalVal'] < (r['Value'] * 0.98))
    avg_margin = safe_pct(tot_del_prof, tot_del_val)
    
    col_left, col_right = st.columns([4.5, 5.5])
    
    with col_left:
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        
        def get_tab5_card(title, pill_text, value, unit, border_color, pill_bg, pill_color, text_color):
            unit_html = f" <span style='font-size:16px; font-weight: 600; color:#94a3b8;'>{unit}</span>" if unit else ""
            return f"""
            <div class="tab5-scope" style="border: 1px solid #e2e8f0; border-left: 6px solid {border_color}; border-radius: 12px; padding: 24px 16px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); background-color: white; height: 100%;">
                <div style="margin-bottom: 16px;">
                    <span style="background-color: {pill_bg}; color: {pill_color}; font-size: 14px; font-weight: 600; padding: 4px 12px; border-radius: 6px; display: inline-block;">{pill_text}</span>
                </div>
                <div style="font-size: 32px; font-weight: 800; color: {text_color}; line-height: 1; margin-bottom: 12px;">
                    {value}{unit_html}
                </div>
                <div style="color: #64748b; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">{title}</div>
            </div>
            """
            
        r1c1, r1c2 = st.columns(2)
        r1c1.markdown(get_tab5_card("TOTAL DELIVERY JOBS", sub_period, safe_fmt(tot_del_jobs), "งาน", "#3b82f6", "#eff6ff", "#2563eb", "#1e3a8a"), unsafe_allow_html=True)
        r1c2.markdown(get_tab5_card("EXPECTED VALUE", sub_period, safe_fmt(tot_del_val), "฿", "#6366f1", "#eef2ff", "#4f46e5", "#312e81"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        r2c1, r2c2 = st.columns(2)
        r2c1.markdown(get_tab5_card("EXPECTED PROFIT", sub_period, safe_fmt(tot_del_prof), "฿", "#14b8a6", "#f0fdfa", "#0d9488", "#115e59"), unsafe_allow_html=True)
        r2c2.markdown(get_tab5_card("AVERAGE MARGIN", sub_period, avg_margin, "", "#22c55e", "#f0fdf4", "#15803d", "#14532d"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
    with col_right:
        
        chart_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        chart_val = [chart_month_data[m]['val'] for m in range(1, 13)]
        chart_prof = [chart_month_data[m]['profit'] for m in range(1, 13)]
        
        fig_del = go.Figure()
        fig_del.add_trace(go.Bar(x=chart_labels, y=chart_val, name='Delivery Value', marker_color='#6366f1', marker_line_width=0))
        fig_del.add_trace(go.Bar(x=chart_labels, y=chart_prof, name='Expected Profit', marker_color='#14b8a6', marker_line_width=0))
        fig_del.update_layout(
            font=dict(family="'Sarabun', sans-serif", size=10), 
            barmode='group', 
            margin=dict(l=10, r=10, t=10, b=20), 
            plot_bgcolor='rgba(0,0,0,0)', 
            yaxis=dict(gridcolor='#f1f5f9', showticklabels=False),
            height=240,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="right", x=1, font=dict(size=10))
        )
        st.plotly_chart(fig_del, use_container_width=True)
        
        st.markdown("""<div class="tab5-scope" style="font-weight: 600; color: #475569; font-size: 14px; margin-top: 8px; text-align: center;">📈 แนวโน้มมูลค่าและกำไรจัดส่ง (Delivery Value & Profit Trend)</div>""", unsafe_allow_html=True)

    st.markdown("""<h3 class="tab5-scope" style="font-weight: bold; color: #1e3a8a; font-size: 16px; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #e2e8f0;">📑 รายการโครงการเตรียมจัดส่ง (แบ่งตามเดือน)</h3>""", unsafe_allow_html=True)
    
    if df_del.empty:
        st.info("ไม่พบข้อมูลกำหนดส่งสินค้าในช่วงเวลานี้")
    else:
        del_parts = []
        del_parts.append('<div class="tab5-scope" style="border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 1px 2px rgba(0,0,0,0.05);"><table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 15px;"><thead style="background-color: #f8fafc; color: #475569; font-weight: bold; text-transform: uppercase; font-size: 12px; border-bottom: 2px solid #e2e8f0;"><tr><th style="padding: 12px; width: 30px; text-align: center;"></th><th style="padding: 12px;">Delivery Month</th><th style="padding: 12px; text-align: center;"># Customers</th><th style="padding: 12px; text-align: center;"># Jobs</th><th style="padding: 12px; text-align: center; color: #ea580c;"><i class="fa-solid fa-file-invoice" style="margin-right: 4px;"></i> รอเปิดบิล</th><th style="padding: 12px; text-align: right;">Expected Value</th><th style="padding: 12px; text-align: right;">Expected Profit</th><th style="padding: 12px; text-align: center;">Avg. Margin</th></tr></thead><tbody>')
        
        for m in sorted(month_data.keys()):
            mD = month_data[m]
            monthRowId = f"del-month-{m}"
            pct_m = safe_pct(mD["profit"], mD["val"])
            num_cust_m = len(mD['custs'])
            
            pending_count = mD['pending_inv']
            if pending_count > 0:
                pending_badge = f'<span style="color: #ef4444; font-weight: bold; font-size: 14px;">🔥 {pending_count} งาน</span>'
            else:
                pending_badge = '<span style="color: #10b981; font-size: 13px; font-weight: bold;">✔️ ครบแล้ว</span>'
            
            del_parts.append(f'<tr style="border-bottom: 1px solid #f1f5f9; cursor: pointer; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#f8fafc\'" onmouseout="this.style.backgroundColor=\'white\'" onclick="toggleDetail(\'{monthRowId}\', this)">')
            del_parts.append(f'<td style="padding: 12px; text-align: center; color: #9ca3af;"><div class="rotate-icon" style="transition: transform 0.2s;">▼</div></td>')
            del_parts.append(f'<td style="padding: 12px; font-weight: 600; color: #312e81; font-size: 15px;">เดือน{TH_MONTHS[m]} (Month {m})</td>')
            del_parts.append(f'<td style="padding: 12px; text-align: center; color: #f59e0b; font-weight: bold; font-size: 15px;">{num_cust_m}</td>')
            del_parts.append(f'<td style="padding: 12px; text-align: center; color: #4b5563; font-size: 15px;">{mD["count"]}</td>')
            del_parts.append(f'<td style="padding: 12px; text-align: center;">{pending_badge}</td>')
            del_parts.append(f'<td style="padding: 12px; text-align: right; font-weight: bold; color: #4338ca; font-size: 15px;">{safe_fmt(mD["val"])}</td>')
            del_parts.append(f'<td style="padding: 12px; text-align: right; font-weight: bold; color: #0d9488; font-size: 15px;">{safe_fmt(mD["profit"])}</td>')
            del_parts.append(f'<td style="padding: 12px; text-align: center; color: #4b5563; font-size: 15px;">{pct_m}</td>')
            del_parts.append('</tr>')
            
            # แก้ไข colspan เป็น 8 เพื่อให้ครอบคลุมคอลัมน์ใหม่
            del_parts.append(f'<tr id="{monthRowId}" class="detail-row" style="display: none; background-color: #f8fafc;"><td colspan="8" style="padding: 0; border-bottom: 2px solid #e2e8f0;">')
            del_parts.append('<div style="padding: 20px 24px; border-left: 4px solid #3b82f6;">')
            del_parts.append('<h4 style="font-size: 15px; font-weight: bold; color: #1e3a8a; margin-bottom: 16px; margin-top: 0;"><span style="margin-right: 6px; font-size: 16px;">📦</span> รายละเอียดโครงการจัดส่ง</h4>')
            
            inner_html = '<div style="max-height: 400px; overflow-y: auto; border: 1px solid #e5e7eb; border-radius: 6px; background: white;"><table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;"><thead style="background-color: #f3f4f6; color: #4b5563; text-transform: uppercase; font-size: 11px; position: sticky; top: 0; z-index: 1;"><tr><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: center;">Del. Date</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: center;">Grp</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Sales Rep</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">SO Number</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #0d9488;">Invoice No. & Status</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Customer</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Prod</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: right;">Value (฿)</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: right;">Profit (฿)</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: center;">% Mg</th></tr></thead><tbody style="background-color: white;">'
            
            jobsByGroup = {}
            for job in mD['jobs']:
                g = job['Group']
                if g not in jobsByGroup: jobsByGroup[g] = {'jobs': [], 'val': 0, 'count': 0}
                jobsByGroup[g]['jobs'].append(job)
                jobsByGroup[g]['val'] += job['Value']
                jobsByGroup[g]['count'] += 1
                
            group_order_del = ['A', 'B', 'C', 'D', 'R', 'COM', 'PD', 'Others']
            for gName in sorted(jobsByGroup.keys(), key=lambda x: group_order_del.index(x) if x in group_order_del else 99):
                gData = jobsByGroup[gName]
                
                inner_html += f'<tr style="background-color: #f1f5f9; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;"><td colspan="10" style="padding: 8px 16px; font-size: 13px; font-weight: bold; color: #312e81;"><span style="display:inline-block; width:16px; text-align:center;">👥</span> GROUP {gName} <span style="font-weight: normal; color: #64748b; margin-left: 8px;">({gData["count"]} งาน | มูลค่า: {safe_fmt(gData["val"])} ฿)</span></td></tr>'
                
                for job in sorted(gData['jobs'], key=lambda x: x['DelDateObj']):
                    invBadge = ''
                    if not job['InvNos']:
                        invBadge = '<span style="color:#f6ad55; font-size:12px; font-style:italic;">รอเปิดบิล</span>'
                    else:
                        isFull = job['InvTotalVal'] >= (job['Value'] * 0.98)
                        if isFull:
                            invBadge = f'<span style="color:#16a34a; font-size:12px; font-weight:bold; margin-right: 4px;">✔️ ครบจำนวน</span> <span style="background-color:#f0fdf4; color:#15803d; padding:2px 6px; border-radius:4px; font-size:11px; border:1px solid #bbf7d0; display:inline-block; max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: bottom;" title="{job["InvNos"]}">{job["InvNos"]}</span>'
                        else:
                            invBadge = f'<span style="color:#ca8a04; font-size:12px; font-weight:bold; margin-right: 4px;">⚠️ บางส่วน</span> <span style="background-color:#fefce8; color:#a16207; padding:2px 6px; border-radius:4px; font-size:11px; border:1px solid #fef08a; display:inline-block; max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: bottom;" title="{job["InvNos"]}">{job["InvNos"]}</span>'
                    
                    pct_mg = safe_pct(job['Profit'], job['Value'])
                    pct_val = (job['Profit'] / job['Value'] * 100) if job['Value'] > 0 else 0
                    pct_color = "color:#ea580c;" if pct_val < 20 else "color:#16a34a;"
                    
                    inner_html += f'<tr style="border-bottom: 1px solid #f3f4f6; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#f8fafc\'" onmouseout="this.style.backgroundColor=\'white\'"><td style="padding: 8px 10px; text-align: center; color: #475569;">{job["DelDateStr"]}</td><td style="padding: 8px 10px; text-align: center; font-weight: bold; color: #475569;">{job["Group"]}</td><td style="padding: 8px 10px; color: #4338ca; font-weight: 500;">{job["SalesRep"]}</td><td style="padding: 8px 10px; font-family: monospace; font-weight: bold; color: #2563eb;">{job["SONumber"]}</td><td style="padding: 8px 10px;">{invBadge}</td><td style="padding: 8px 10px; color: #334155;">{escape_html(job["Customer"])}</td><td style="padding: 8px 10px; color: #475569;">{job["Product"]}</td><td style="padding: 8px 10px; text-align: right; font-weight: bold; color: #4338ca;">{safe_fmt(job["Value"])}</td><td style="padding: 8px 10px; text-align: right; font-weight: bold; color: #0d9488;">{safe_fmt(job["Profit"])}</td><td style="padding: 8px 10px; text-align: center; font-weight: bold; {pct_color}">{pct_mg}</td></tr>'
                    
            inner_html += '</tbody></table></div></div></td></tr>'
            del_parts.append(inner_html)

        tot_pct_all = safe_pct(tot_del_prof, tot_del_val)
        del_parts.append('</tbody><tfoot style="background-color: #f8fafc; font-weight: bold; font-size: 15px; border-top: 2px solid #e2e8f0;"><tr><td colspan="2" style="padding: 14px 12px; text-align: right; text-transform: uppercase; color: #475569;">Total</td>')
        del_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #f59e0b;">{tot_del_custs}</td>')
        del_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #475569;">{tot_del_jobs}</td>')
        del_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #ef4444; font-size: 16px;">{tot_pending_inv}</td>')
        del_parts.append(f'<td style="padding: 14px 12px; text-align: right; color: #ea580c;">{safe_fmt(tot_del_val)}</td>')
        del_parts.append(f'<td style="padding: 14px 12px; text-align: right; color: #0d9488;">{safe_fmt(tot_del_prof)}</td>')
        del_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #475569;">{tot_pct_all}</td></tr></tfoot></table></div>')

        components.html(f"{COMMON_HTML_HEAD}<body>{''.join(del_parts)}</body>", height=700, scrolling=True)

with tab6:
    try:
        st.markdown("""
            <div style="border-left: 4px solid #a855f7; background-color: #faf5ff; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); display: flex; align-items: center; flex-wrap: wrap; gap: 8px; font-family: 'Sarabun', sans-serif;">
                <h2 style="color: #6b21a8; font-size: 18px; margin: 0; font-family: 'Sarabun', sans-serif;">🔎 ส่องรายละเอียดของงาน (SO INFO)</h2>
                <span style="color: #7e22ce; font-size: 15px; font-family: 'Sarabun', sans-serif;">| สถิติลูกค้าใหม่และลูกค้าที่กลับมาซื้อซ้ำ (>5 ปี) พร้อมวิเคราะห์การขายแยกตามพนักงานขาย</span>
            </div>
        """, unsafe_allow_html=True)

        new_cust_counts = {}
        winback_counts = {}
        global_new_cust = set()
        global_winback_cust = set()
        
        rep_jobs = {}
        
        for row in df_so_year.sort_values(['Month']).itertuples(index=False):
            month = int(row.Month)
            if not (1 <= month <= 12): continue
            
            # นำเงื่อนไข if month not in selected_month ออกจากส่วนเริ่มต้น 
            # เพื่อให้โค้ดสามารถนับจำนวนลูกค้าใหม่และ Winback ได้ตลอดทั้งปี

            cust = row.Customer
            rep = row.SalesRep if pd.notna(row.SalesRep) and str(row.SalesRep).strip() != '' else 'Unknown'
            so_date = row.SODate
            val = float(row.Actual) if pd.notna(row.Actual) else 0.0
            prof = float(row.Margin) if pd.notna(row.Margin) else 0.0

            is_winback = False
            status_html = "-"
            
            if pd.notna(so_date):
                dates = cust_dates.get(cust, [])
                past_dates = [d for d in dates if d < so_date]
                last_d = max(past_dates) if past_dates else None
                if last_d and (so_date - last_d).days / 365.25 > 5.0:
                    is_winback = True
                    status_html = '<span style="background-color: #ffedd5; color: #c2410c; border: 1px solid #fdba74; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: bold;">WINBACK</span>'
                elif selected_year != 'All' and str(getattr(row, 'RegYear', '')) == str(selected_year):
                    status_html = '<span style="background-color: #f3e8ff; color: #7e22ce; border: 1px solid #d8b4fe; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: bold;">NEW</span>'

            # --- ส่วนที่ 1: คำนวณลูกค้าใหม่ / Win-back (ไม่ต้องอิงตัวกรองเดือน) ---
            if is_winback:
                cust_key = f"{rep}-{cust}"
                if cust_key not in global_winback_cust:
                    global_winback_cust.add(cust_key)
                    if rep not in winback_counts: winback_counts[rep] = {m:0 for m in range(1,13)}
                    winback_counts[rep][month] += 1
            else:
                is_new_year = (str(getattr(row, 'RegYear', '')) == str(selected_year)) if selected_year != 'All' else True
                reg_m_val = getattr(row, 'RegMonth', 0)
                if is_new_year and pd.notna(reg_m_val):
                    reg_m = int(reg_m_val)
                    if 1 <= reg_m <= 12:
                        cust_key = f"{rep}-{cust}"
                        if cust_key not in global_new_cust:
                            global_new_cust.add(cust_key)
                            if rep not in new_cust_counts: new_cust_counts[rep] = {m:0 for m in range(1,13)}
                            new_cust_counts[rep][reg_m] += 1

            # --- ส่วนที่ 2: คำนวณรายละเอียดงานขาย Job Detail (ต้องอิงตัวกรองเดือนเท่านั้น) ---
            if month in selected_month:
                q_no = str(getattr(row, 'QuotationNo', '-')).strip()
                if q_no.lower() == 'nan' or not q_no: q_no = '-'

                if rep not in rep_jobs:
                    rep_jobs[rep] = {'val': 0, 'prof': 0, 'jobs': 0, 'custs': set(), 'cust_map': {}, 'inds_map': {}, 'prod_map': {}, 'details': []}

                rep_jobs[rep]['val'] += val; rep_jobs[rep]['prof'] += prof; rep_jobs[rep]['jobs'] += 1; rep_jobs[rep]['custs'].add(cust)
                rep_jobs[rep]['cust_map'][cust] = rep_jobs[rep]['cust_map'].get(cust, 0) + val
                rep_jobs[rep]['inds_map'][row.Industry] = rep_jobs[rep]['inds_map'].get(row.Industry, 0) + val
                rep_jobs[rep]['prod_map'][row.Product] = rep_jobs[rep]['prod_map'].get(row.Product, 0) + val

                rep_jobs[rep]['details'].append({'so': row.SONumber, 'cust': cust, 'prod': row.Product, 'quote': q_no, 'status': status_html, 'val': val})

        st.markdown("""<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 12px; font-family: 'Sarabun', sans-serif;"><h3 style="font-weight: bold; color: #1e3a8a; font-size: 16px; margin: 0; font-family: 'Sarabun', sans-serif;">🌟 สถิติลูกค้าใหม่ และ ลูกค้าที่กลับมาซื้อซ้ำ (>5 ปี) รายบุคคล</h3><span style="font-size: 13px; color: #475569; background-color: #f1f5f9; padding: 2px 8px; border-radius: 9999px; font-style: italic; font-family: 'Sarabun', sans-serif;">* Logic: New Cust จะไม่นับซ้ำกับรายชื่อ Win-back</span></div>""", unsafe_allow_html=True)
        
        all_reps_in_stats = set(new_cust_counts.keys()).union(set(winback_counts.keys()))
        combined_stats = []
        for r_name in all_reps_in_stats:
            nc = new_cust_counts.get(r_name, {m:0 for m in range(1,13)})
            wb = winback_counts.get(r_name, {m:0 for m in range(1,13)})
            tot_nc = sum(nc.values())
            tot_wb = sum(wb.values())
            combined_stats.append({
                'rep': r_name, 'nc': nc, 'wb': wb, 
                'tot_nc': tot_nc, 'tot_wb': tot_wb, 'tot_all': tot_nc + tot_wb
            })
        
        combined_stats.sort(key=lambda x: x['tot_all'], reverse=True)

        cw_parts = []
        # เพิ่ม font-family: 'Sarabun' และเพิ่มขนาด font-size พื้นฐานเป็น 13px พร้อมกำหนด Width ให้สมดุล
        cw_parts.append('<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 24px;"><table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; font-family: \'Sarabun\', sans-serif; background-color: white;"><thead style="background-color: #f8fafc; color: #475569; font-size: 12px; font-weight: bold; border-bottom: 1px solid #e2e8f0; text-transform: uppercase;"><tr><th style="padding: 8px 12px; border-right: 1px solid #e2e8f0; text-align: left; width: 16%;">Sales Name</th><th style="padding: 8px 10px; background-color: #f1f5f9; border-right: 1px solid #e2e8f0; width: 6%;">Total</th><th style="padding: 8px 12px; border-right: 1px solid #e2e8f0; text-align: left; width: 12%;">Customer Type</th>')
        for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
            # ขยายความกว้างและ padding คอลัมน์เดือนให้กว้างขึ้น
            cw_parts.append(f'<th style="padding: 8px 8px; width: 5.5%;">{m}</th>')
        cw_parts.append('</tr></thead><tbody>')

        if not combined_stats:
            cw_parts.append('<tr><td colspan="15" style="text-align: center; padding: 16px; color: #9ca3af; font-style: italic; font-size: 13px;">ไม่พบสถิติลูกค้าใหม่ หรือ Win-back ในช่วงเวลานี้</td></tr>')
        else:
            grand_nc = {m:0 for m in range(1,13)}; grand_tot_nc = 0
            grand_wb = {m:0 for m in range(1,13)}; grand_tot_wb = 0
            
            for st_data in combined_stats:
                rep_name = st_data['rep']
                nc = st_data['nc']
                wb = st_data['wb']
                tot_all = st_data['tot_all']
                
                # Row 1: New Cust
                cw_parts.append(f'<tr style="border-bottom: 1px solid #f8fafc; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#faf5ff\'" onmouseout="this.style.backgroundColor=\'white\'">')
                # ขยายชื่อเซลล์เป็น 14px
                cw_parts.append(f'<td rowspan="2" style="padding: 8px 12px; border-right: 1px solid #e2e8f0; text-align: left; font-weight: 600; color: #1e293b; border-bottom: 1px solid #e2e8f0; vertical-align: middle; background-color: white; font-size: 14px;">{rep_name}</td>')
                # เพิ่มคอลัมน์ Total (รวม NC+WB) ย้ายมาอยู่ทางซ้าย (rowspan=2)
                cw_parts.append(f'<td rowspan="2" style="padding: 8px 10px; border-right: 1px solid #e2e8f0; text-align: center; font-weight: 800; color: #1e40af; border-bottom: 1px solid #e2e8f0; vertical-align: middle; background-color: #eff6ff; font-size: 15px;">{tot_all}</td>')
                # ขยายประเภทลูกค้าเป็น 13px, ป้าย New เป็น 10px
                cw_parts.append('<td style="padding: 6px 12px; border-right: 1px solid #f1f5f9; text-align: left; color: #7e22ce; font-size: 13px; font-weight: 500;"><span style="background-color: #60a5fa; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px; font-weight: bold; margin-right: 6px; vertical-align: middle;">NEW</span>New Customers</td>')
                for m in range(1, 13):
                    v = nc[m]; grand_nc[m] += v
                    c_style = "color: #7e22ce; font-weight: bold; background-color: #faf5ff;" if v > 0 else "color: #cbd5e1;"
                    # ขยายตัวเลขเดือนเป็น 13px และเพิ่ม padding
                    cw_parts.append(f'<td style="padding: 6px 8px; font-size: 13px; {c_style}">{v if v > 0 else "-"}</td>')
                grand_tot_nc += st_data['tot_nc']
                cw_parts.append('</tr>')
                
                # Row 2: Win-back
                cw_parts.append(f'<tr style="border-bottom: 1px solid #e2e8f0; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#fff7ed\'" onmouseout="this.style.backgroundColor=\'white\'">')
                cw_parts.append('<td style="padding: 6px 12px; border-right: 1px solid #f1f5f9; text-align: left; color: #c2410c; font-size: 13px; font-weight: 500;"><span style="display:inline-block; width:16px; text-align:center; font-size: 12px; margin-right: 4px;">🏆</span>Win-back (>5Y)</td>')
                for m in range(1, 13):
                    v = wb[m]; grand_wb[m] += v
                    c_style = "color: #c2410c; font-weight: bold; background-color: #fff7ed;" if v > 0 else "color: #cbd5e1;"
                    cw_parts.append(f'<td style="padding: 6px 8px; font-size: 13px; {c_style}">{v if v > 0 else "-"}</td>')
                grand_tot_wb += st_data['tot_wb']
                cw_parts.append('</tr>')

            # Footer
            cw_parts.append('</tbody><tfoot style="font-weight: bold; font-size: 14px;">')
            
            # Footer Row 1: Grand Total New
            cw_parts.append('<tr style="background-color: #f3e8ff; color: #581c87; border-bottom: 1px solid #e9d5ff;">')
            cw_parts.append('<td rowspan="2" style="padding: 10px 12px; border-right: 1px solid #e2e8f0; text-align: left; background-color: #f1f5f9; color: #1e293b; font-size: 14px; vertical-align: middle;">GRAND TOTAL</td>')
            grand_total_all = grand_tot_nc + grand_tot_wb
            cw_parts.append(f'<td rowspan="2" style="padding: 8px 10px; border-right: 1px solid #e2e8f0; text-align: center; font-weight: 800; color: #1e3a8a; background-color: #e0e7ff; font-size: 15px; vertical-align: middle;">{grand_total_all}</td>')
            cw_parts.append('<td style="padding: 8px 12px; border-right: 1px solid #e9d5ff; text-align: left;"><span style="background-color: #60a5fa; color: white; padding: 1px 4px; border-radius: 2px; font-size: 10px; font-weight: bold; margin-right: 6px; vertical-align: middle;">NEW</span>TOTAL NEW CUST</td>')
            for m in range(1, 13):
                cw_parts.append(f'<td style="padding: 8px 8px; font-size: 13px;">{grand_nc[m] if grand_nc[m] > 0 else "-"}</td>')
            cw_parts.append('</tr>')

            # Footer Row 2: Grand Total Win-back
            cw_parts.append('<tr style="background-color: #ffedd5; color: #9a3412;">')
            cw_parts.append('<td style="padding: 8px 12px; border-right: 1px solid #fed7aa; text-align: left;"><span style="display:inline-block; width:16px; text-align:center; font-size: 12px; margin-right: 4px;">🏆</span>TOTAL WIN-BACK</td>')
            for m in range(1, 13):
                cw_parts.append(f'<td style="padding: 8px 8px; font-size: 13px;">{grand_wb[m] if grand_wb[m] > 0 else "-"}</td>')
            cw_parts.append('</tr>')
            
            cw_parts.append('</tfoot></table></div>')
        
        st.markdown("".join(cw_parts), unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        # --- ส่วนที่ 3: รายละเอียดงานขายรายโครงการ (Job Detail) ---
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; margin-top: 24px; margin-bottom: 12px; font-family: 'Sarabun', sans-serif;">
                <h3 style="font-weight: bold; color: #1f2937; font-size: 16px; margin: 0; font-family: 'Sarabun', sans-serif;">📑 รายละเอียดงานขายรายโครงการ (Job Detail)</h3>
                <span style="font-size: 13px; color: #4338ca; background-color: #e0e7ff; padding: 4px 10px; border-radius: 6px; font-weight: 600; border: 1px solid #c7d2fe;">
                    <i class="fa-solid fa-filter" style="margin-right: 4px;"></i> {s_month_txt} | {s_grp} | {s_year}
                </span>
            </div>
        """, unsafe_allow_html=True)

        if not rep_jobs:
            st.info("ไม่พบข้อมูลรายละเอียดงานขาย (Job Detail) ในช่วงเวลา/เงื่อนไขที่เลือก")
        else:
            def build_top_html(d_map, title, icon, color_class, bg_header):
                sorted_items = sorted(d_map.items(), key=lambda x: x[1], reverse=True)[:10]
                res = f'<div style="background-color: white; border: 1px solid #e5e7eb; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); height: 210px; display: flex; flex-direction: column;"><h4 style="font-size: 15px; font-weight: bold; color: {color_class}; border-bottom: 1px solid #e5e7eb; background-color: {bg_header}; padding: 10px; margin: 0;">{icon} {title}</h4><div style="flex: 1; overflow-y: auto; padding: 4px 8px;">'
                if not sorted_items: res += '<div style="color: #9ca3af; font-style: italic; font-size: 14px; padding: 8px; text-align: center;">No data</div>'
                else:
                    for k, v in sorted_items: res += f'<div style="display: flex; justify-content: space-between; font-size: 14px; border-bottom: 1px solid #f9fafb; padding: 6px 0;"><span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 65%; color: #4b5563;" title="{k}">{k}</span><span style="font-weight: bold; color: {color_class};">{safe_fmt(v)}</span></div>'
                res += '</div></div>'
                return res

            tot_val = 0; tot_prof = 0; tot_jobs = 0; global_custs = set()

            jd_parts = []
            jd_parts.append('<div style="border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 1px 2px rgba(0,0,0,0.05);"><table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 15px;"><thead style="background-color: #f8fafc; color: #475569; font-weight: bold; text-transform: uppercase; font-size: 13px; border-bottom: 2px solid #e2e8f0;"><tr><th style="padding: 12px; width: 30px; text-align: center;"></th><th style="padding: 12px;">Sales Name</th><th style="padding: 12px; text-align: right;">Total Sales</th><th style="padding: 12px; text-align: right;">Profit</th><th style="padding: 12px; text-align: center;">% Margin</th><th style="padding: 12px; text-align: center;"># Cust</th><th style="padding: 12px; text-align: center;"># Jobs</th></tr></thead><tbody>')

            for i, (rep, data) in enumerate(sorted(rep_jobs.items(), key=lambda x: x[1]['val'], reverse=True)):
                tot_val += data['val']; tot_prof += data['prof']; tot_jobs += data['jobs']
                for c in data['custs']: global_custs.add(c)

                pct_margin = safe_pct(data['prof'], data['val'])
                row_id = f"so-detail-{i}"

                top_cust_html = build_top_html(data['cust_map'], 'Top 10 Customers', '👑', '#b45309', '#fefce8')
                top_inds_html = build_top_html(data['inds_map'], 'Top 10 Industries', '🏭', '#1d4ed8', '#eff6ff')
                top_prod_html = build_top_html(data['prod_map'], 'Top Products (Value Add)', '📦', '#4338ca', '#eef2ff')

                tx_html = '<div style="max-height: 250px; overflow-y: auto; border: 1px solid #e5e7eb; border-radius: 6px; background: white;"><table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;"><thead style="background-color: #f3f4f6; color: #4b5563; text-transform: uppercase; font-size: 12px; position: sticky; top: 0; z-index: 1;"><tr><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">SO No.</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb; color: #3b82f6;">Quotation No.</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Customer</th><th style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Product</th><th style="padding: 10px; text-align: center; border-bottom: 1px solid #e5e7eb;">Status</th><th style="padding: 10px; text-align: right; border-bottom: 1px solid #e5e7eb;">Amount (฿)</th></tr></thead><tbody style="background-color: white;">'
                
                # ทยอยเพิ่มข้อมูลธุรกรรมเพื่อป้องกัน String ยาวเกิน
                for tx in data['details']:
                    tx_html += f'<tr style="border-bottom: 1px solid #f3f4f6; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#f9fafb\'" onmouseout="this.style.backgroundColor=\'white\'">'
                    tx_html += f'<td style="padding: 8px 10px; font-family: monospace; font-weight: bold; color: #4f46e5;">{tx["so"]}</td>'
                    tx_html += f'<td style="padding: 8px 10px; font-family: monospace; color: #3b82f6;">{tx["quote"]}</td>'
                    tx_html += f'<td style="padding: 8px 10px; color: #374151;">{escape_html(tx["cust"])}</td>'
                    tx_html += f'<td style="padding: 8px 10px; color: #4b5563;">{tx["prod"]}</td>'
                    tx_html += f'<td style="padding: 8px 10px; text-align: center;">{tx["status"]}</td>'
                    tx_html += f'<td style="padding: 8px 10px; text-align: right; font-weight: bold; color: #4338ca;">{safe_fmt(tx["val"])}</td>'
                    tx_html += '</tr>'
                tx_html += '</tbody></table></div>'

                # หั่น String ยาวในส่วนของกล่องแสดงข้อมูลตัวแทนขาย
                jd_parts.append(f'<tr style="border-bottom: 1px solid #f1f5f9; cursor: pointer; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#f8fafc\'" onmouseout="this.style.backgroundColor=\'white\'" onclick="toggleDetail(\'{row_id}\', this)">')
                jd_parts.append(f'<td style="padding: 12px; text-align: center; color: #9ca3af;"><div class="rotate-icon" style="transition: transform 0.2s;">▼</div></td>')
                jd_parts.append(f'<td style="padding: 12px; font-weight: 600; color: #374151; font-size: 15px;">{rep}</td>')
                jd_parts.append(f'<td style="padding: 12px; text-align: right; font-weight: bold; color: #4338ca; font-size: 15px;">{safe_fmt(data["val"])}</td>')
                jd_parts.append(f'<td style="padding: 12px; text-align: right; font-weight: bold; color: #0d9488; font-size: 15px;">{safe_fmt(data["prof"])}</td>')
                jd_parts.append(f'<td style="padding: 12px; text-align: center; color: #4b5563; font-size: 15px;">{pct_margin}</td>')
                jd_parts.append(f'<td style="padding: 12px; text-align: center; color: #4b5563; font-size: 15px;">{len(data["custs"])}</td>')
                jd_parts.append(f'<td style="padding: 12px; text-align: center; color: #4b5563; font-size: 15px;">{data["jobs"]}</td></tr>')
                
                jd_parts.append(f'<tr id="{row_id}" class="detail-row" style="display: none; background-color: #f8fafc;"><td colspan="7" style="padding: 0; border-bottom: 2px solid #e2e8f0;">')
                jd_parts.append('<div style="padding: 20px 24px; border-left: 4px solid #818cf8;"><div style="display: flex; gap: 16px; margin-bottom: 16px;">')
                jd_parts.append(f'<div style="flex: 1; min-width: 0;">{top_cust_html}</div><div style="flex: 1; min-width: 0;">{top_inds_html}</div><div style="flex: 1; min-width: 0;">{top_prod_html}</div></div>')
                jd_parts.append('<h4 style="font-size: 15px; font-weight: bold; color: #4b5563; margin-bottom: 10px; margin-top: 0;">SO Transaction Details</h4>')
                jd_parts.append(tx_html)
                jd_parts.append('</div></td></tr>')

            tot_pct = safe_pct(tot_prof, tot_val)
            jd_parts.append('</tbody><tfoot style="background-color: #f8fafc; font-weight: bold; font-size: 15px; border-top: 2px solid #e2e8f0;"><tr><td colspan="2" style="padding: 14px 12px; text-align: right; text-transform: uppercase; color: #475569;">Total</td>')
            jd_parts.append(f'<td style="padding: 14px 12px; text-align: right; color: #ea580c;">{safe_fmt(tot_val)}</td>')
            jd_parts.append(f'<td style="padding: 14px 12px; text-align: right; color: #0d9488;">{safe_fmt(tot_prof)}</td>')
            jd_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #475569;">{tot_pct}</td>')
            jd_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #475569;">{len(global_custs)}</td>')
            jd_parts.append(f'<td style="padding: 14px 12px; text-align: center; color: #475569;">{tot_jobs}</td></tr></tfoot></table></div>')

            components.html(f"{COMMON_HTML_HEAD}<body>{''.join(jd_parts)}</body>", height=900, scrolling=True)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการประมวลผล (Tab 6): {str(e)}")

# ------------------------------------------
# TAB 7: ประวัติลูกค้า (Customer History)
# ------------------------------------------
with tab7:
    try:
        import json
        header_placeholder = st.empty()
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            search_cust = st.text_input("🔍 พิมพ์ค้นหาชื่อลูกค้า...", "").lower()
        with col_s2:
            search_prod = st.text_input("🔍 พิมพ์ค้นหารุ่นสินค้า หรือรหัสสินค้า...", "").lower()

        ch = {}
        for d in df_so_all.itertuples(index=False):
            if selected_group != "All" and d.Group != selected_group: 
                continue
            
            c_name = d.Customer
            if c_name not in ch:
                ch[c_name] = {
                    'name': c_name, 'totalVal': 0.0, 'soCount': 0, 'history': [],
                    'lastDate': pd.Timestamp('1900-01-01'), 'lastRep': '', 'pdTypes': set(),
                    'search_str_prod': '', 'ind': str(d.Industry) if pd.notna(d.Industry) else 'Unknown'
                }
                
            val_d = float(d.Actual) if pd.notna(d.Actual) else 0.0
            ch[c_name]['totalVal'] += val_d
            ch[c_name]['soCount'] += 1
            ch[c_name]['history'].append({'Year': d.Year, 'Month': d.Month, 'SONumber': d.SONumber, 'Product': d.Product, 'Industry': d.Industry, 'SalesRep': d.SalesRep, 'Actual': val_d, 'QuotationNo': getattr(d, 'QuotationNo', '-')})
            
            so_date = d.SODate
            if pd.notna(so_date) and so_date > ch[c_name]['lastDate']:
                ch[c_name]['lastDate'] = so_date
                ch[c_name]['lastRep'] = str(d.SalesRep)
                
            related_sois = soi_map.get(d.SONumber, [])
            soi_text = " ".join([f"{s['pdCode']} {s['pdName']} {s['pdTypeName']}" for s in related_sois]).lower()
            
            for s in related_sois:
                if s['pdTypeName'] and s['pdTypeName'] != 'Unknown':
                    ch[c_name]['pdTypes'].add(s['pdTypeName'])
                    
            ch[c_name]['search_str_prod'] += f" {str(d.Product).lower()} {str(d.SONumber).lower()} {soi_text}"

        all_industries = sorted(list(set(str(c['history'][0]['Industry']) for c in ch.values() if c['history'])))
        all_reps = sorted(list(set(str(c['lastRep']) for c in ch.values() if c['lastRep'])))
        all_prods = sorted(list(set(str(h['Product']) for c in ch.values() for h in c['history'] if pd.notna(h['Product']) and str(h['Product']) != 'Unknown')))
        all_types = ["สินค้าสำเร็จรูป", "สินค้ากึ่งสำเร็จรูป", "บริการ", "รายได้อื่นๆ"]

        f1, f2, f3, f4 = st.columns([3, 4, 2, 2])
        cur_ind = f1.selectbox("🏭 อุตสาหกรรม:", ["All"] + all_industries)
        cur_rep = f2.selectbox("👤 พนักงานขาย:", ["All"] + all_reps)
        cur_prod = f3.selectbox("📦 ผลิตภัณฑ์:", ["All"] + all_prods)
        cur_type = f4.selectbox("🏷️ ประเภท (Type):", ["All"] + all_types)

        display_list = list(ch.values())
        if cur_ind != 'All': display_list = [c for c in display_list if c['ind'] == cur_ind]
        if cur_rep != 'All': display_list = [c for c in display_list if c['lastRep'] == cur_rep]
        if cur_prod != 'All': display_list = [c for c in display_list if any(h['Product'] == cur_prod for h in c['history'])]
        if cur_type != 'All': display_list = [c for c in display_list if cur_type in c['pdTypes']]
        
        if search_cust: display_list = [c for c in display_list if search_cust in c['name'].lower()]
        if search_prod: display_list = [c for c in display_list if search_prod in c['search_str_prod']]

        display_list.sort(key=lambda x: x['totalVal'], reverse=True)
        total_found = len(display_list)
        limit = total_found if (search_cust or search_prod) else 100
        
        warning_html = ""
        if not (search_cust or search_prod) and total_found > 100:
            warning_html = f'<div style="margin-top: 8px;"><span style="color: #ea580c; font-size: 13px; font-weight: 600;"><i class="fa-solid fa-triangle-exclamation" style="margin-right: 4px;"></i> แสดง 100 รายการแรกจากทั้งหมด {total_found} รายการ (กรุณาพิมพ์ค้นหาเพิ่มเติมเพื่อดูข้อมูลเฉพาะ)</span></div>'

        header_placeholder.markdown(f"""
            <div style='margin-bottom: 24px; font-family: "Sarabun", sans-serif;'>
                <span style='font-size: 20px; font-weight: bold; color: #2B3467;'>📇 ประวัติการซื้อลูกค้าทั้งหมด (Customer SO History)</span>
                <span style='font-size: 14px; color: #64748b;'>| ดูประวัติการเปิดใบสั่งขาย (SO) และเจาะลึกถึงรายละเอียดสินค้า (SOI) ของลูกค้าแต่ละราย</span>
                {warning_html}
            </div>
        """, unsafe_allow_html=True)
        
        display_list = display_list[:limit]

        if not display_list:
            st.info("ไม่พบข้อมูลลูกค้าจากคำค้นหาหรือตัวกรองนี้")
        else:
            hist_parts = []
            hist_parts.append('<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 1px 2px rgba(0,0,0,0.05); font-family: \'Sarabun\', sans-serif;"><table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;"><thead style="background-color: #eef2ff; color: #312e81; font-weight: bold; text-transform: uppercase; font-size: 11px; border-bottom: 2px solid #c7d2fe;"><tr><th style="padding: 8px 10px; width: 30px; text-align: center;"></th><th style="padding: 8px 10px;">Customer Name</th><th style="padding: 8px 10px; text-align: center;">Industry</th><th style="padding: 8px 10px; text-align: center;">Total SOs</th><th style="padding: 8px 10px; text-align: right;">Historical LTV</th><th style="padding: 8px 10px; text-align: center;">Last Purchase</th><th style="padding: 8px 10px;">Last Rep</th><th style="padding: 8px 10px; text-align: center; width: 120px;">Action</th></tr></thead><tbody>')

            for i, c in enumerate(display_list):
                rid = f"hist-cust-{i}"
                sorted_hist = sorted(c['history'], key=lambda x: (x['Year'], x['Month']), reverse=True)
                prod_groups = {}
                
                # =========================================================
                # 🔥 จัดเตรียมข้อมูลสำหรับการวิเคราะห์ AI ขั้นสูง (ดึงจาก History)
                # =========================================================
                prod_mix = {}
                hist_text = ""
                
                for h_idx, h in enumerate(sorted_hist):
                    p = h['Product'] or "Unknown"
                    if cur_prod != 'All' and p != cur_prod: continue
                    
                    rel_sois = soi_map.get(h['SONumber'], [])
                    if cur_type != 'All':
                        rel_sois = [s for s in rel_sois if s['pdTypeName'] == cur_type]
                    
                    if search_prod:
                        is_so_match = search_prod in f"{p} {h['SONumber']}".lower()
                        rel_sois = [s for s in rel_sois if is_so_match or search_prod in f"{s['pdCode']} {s['pdName']} {s['pdTypeName']}".lower()]
                        if not is_so_match and not rel_sois:
                            continue
                    
                    val_h = float(h['Actual']) if pd.notna(h['Actual']) else 0.0
                    
                    # สะสมข้อมูลสำหรับ AI 
                    if str(p).strip() != "" and str(p) != "Unknown" and str(p) != "nan":
                        prod_mix[p] = prod_mix.get(p, 0.0) + val_h
                    if h_idx < 20:
                        hist_text += f"- {int(h.get('Month', 0))}/{h.get('Year', '-')} | {p} | {val_h:,.0f} THB\n"
                    
                    if p not in prod_groups:
                        prod_groups[p] = {'totalVal': 0, 'count': 0, 'totalQty': 0, 'items': {}}
                        
                    prod_groups[p]['totalVal'] += val_h
                    prod_groups[p]['count'] += 1
                    
                    if not rel_sois:
                        dummy = 'N/A'
                        if dummy not in prod_groups[p]['items']:
                            msg = "No item detail"
                            if cur_type != 'All': msg = f"ไม่พบสินค้าประเภท '{cur_type}'"
                            elif search_prod: msg = "ไม่พบรายละเอียดสินค้าที่ตรงกับคำค้นหา"
                            prod_groups[p]['items'][dummy] = {'pdName': msg, 'pdTypeName': '-', 'totalQty': 0, 'txs': []}
                        
                        q_no = str(h.get('QuotationNo', '-')).strip()
                        if q_no.lower() == 'nan' or not q_no: q_no = '-'
                        
                        prod_groups[p]['items'][dummy]['txs'].append({
                            'date': f"{int(h['Month'])}/{h['Year']}", 'so': h['SONumber'], 'quote': q_no, 'qty': '-', 'rep': h['SalesRep'], 'val': val_h
                        })
                    else:
                        for soi in rel_sois:
                            code = soi['pdCode'] or 'Unknown'
                            if code not in prod_groups[p]['items']:
                                prod_groups[p]['items'][code] = {'pdName': soi['pdName'], 'pdTypeName': soi['pdTypeName'], 'totalQty': 0, 'txs': []}
                            
                            try:
                                qty = float(str(soi['qty']).replace(',','')) if pd.notna(soi['qty']) else 0.0
                            except:
                                qty = 0.0
                                
                            prod_groups[p]['items'][code]['totalQty'] += qty
                            prod_groups[p]['totalQty'] += qty
                            
                            q_no = str(h.get('QuotationNo', '-')).strip()
                            if q_no.lower() == 'nan' or not q_no: q_no = '-'
                            
                            prod_groups[p]['items'][code]['txs'].append({
                                'date': f"{int(h['Month'])}/{h['Year']}", 'so': h['SONumber'], 'quote': q_no, 'qty': format_num_short(soi['qty']), 'rep': h['SalesRep'], 'val': val_h
                            })
                
                nested_html = ""
                for p_idx, (p_name, p_data) in enumerate(sorted(prod_groups.items(), key=lambda x: x[1]['totalVal'], reverse=True)):
                    nested_html += f"""
                    <div style="margin-bottom: 12px; border: 1px solid #c7d2fe; border-radius: 6px; overflow: hidden; background-color: white; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                        <div style="background-color: #e0e7ff; padding: 6px 12px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #c7d2fe;">
                            <span style="font-weight: bold; color: #312e81; font-size: 13px;">📦 Product: {p_name}</span>
                            <span style="font-size: 12px; color: #3730a3; font-weight: bold; background-color: white; padding: 2px 8px; border-radius: 4px; border: 1px solid #c7d2fe;">
                                {p_data['count']} SOs | Total Qty: <span style="color: #db2777;">{format_num_short(p_data['totalQty'])}</span> | Total: {safe_fmt(p_data['totalVal'])} ฿
                            </span>
                        </div>
                        <div style="overflow-x: auto;">
                            <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 12px;">
                                <thead style="background-color: #fce7f3; color: #9d174d; border-bottom: 1px solid #fbcfe8; font-size: 11px;">
                                    <tr>
                                        <th style="padding: 6px; width: 30px; text-align: center;"></th>
                                        <th style="padding: 6px; border-right: 1px solid #fbcfe8;">Type</th>
                                        <th style="padding: 6px; border-right: 1px solid #fbcfe8;">Item Code</th>
                                        <th style="padding: 6px; border-right: 1px solid #fbcfe8;">Description (PdName)</th>
                                        <th style="padding: 6px; border-right: 1px solid #fbcfe8; text-align: center;">Last Purchase</th>
                                        <th style="padding: 6px; text-align: center;">Total Qty</th>
                                    </tr>
                                </thead>
                                <tbody>
                    """
                    
                    for item_idx, (item_code, item_data) in enumerate(sorted(p_data['items'].items(), key=lambda x: x[1]['totalQty'], reverse=True)):
                        item_rid = f"item-hist-{i}-{p_idx}-{item_idx}"
                        last_d = item_data['txs'][0]['date'] if item_data['txs'] else '-'
                        qty_str = format_num_short(item_data['totalQty']) if item_data['totalQty'] > 0 else '-'
                        
                        # หั่น String ป้องกันปัญหาขีดจำกัด AI
                        nested_html += f'<tr style="border-bottom: 1px solid #fdf2f8; cursor: pointer; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#fdf2f8\'" onmouseout="this.style.backgroundColor=\'white\'" onclick="toggleDetail(\'{item_rid}\', this)">'
                        nested_html += f'<td style="padding: 4px 6px; text-align: center;"><div class="rotate-icon" style="transition: transform 0.2s; color: #9ca3af;">▼</div></td>'
                        nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #fdf2f8; color: #4b5563; font-size: 12px;">{item_data["pdTypeName"]}</td>'
                        nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #fdf2f8; font-family: monospace; font-weight: bold; color: #4338ca; font-size: 12px;">{item_code}</td>'
                        nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #fdf2f8; color: #374151; font-size: 12px;">{escape_html(item_data["pdName"])}</td>'
                        nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #fdf2f8; text-align: center; color: #6b7280; font-size: 12px;">{last_d}</td>'
                        nested_html += f'<td style="padding: 4px 6px; text-align: center; font-weight: bold; color: #db2777; background-color: #fdf2f8; font-size: 12px;">{qty_str}</td></tr>'
                        
                        nested_html += f"""
                        <tr id="{item_rid}" class="detail-row" style="display: none; background-color: #f8fafc;">
                            <td colspan="6" style="padding: 0; border-bottom: 2px solid #e0e7ff;">
                                <div style="padding: 8px 8px 8px 40px;">
                                    <table style="width: 100%; border: 1px solid #e2e8f0; background-color: white; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); font-size: 11px;">
                                        <thead style="background-color: #f1f5f9; color: #475569; border-bottom: 1px solid #e2e8f0;">
                                            <tr>
                                                <th style="padding: 4px 6px; border-right: 1px solid #e2e8f0; text-align: center;">Date</th>
                                                <th style="padding: 4px 6px; border-right: 1px solid #e2e8f0;">SO / Job No.</th>
                                                <th style="padding: 4px 6px; border-right: 1px solid #e2e8f0; color: #2563eb;">Quotation No.</th>
                                                <th style="padding: 4px 6px; border-right: 1px solid #e2e8f0; text-align: center; color: #db2777;">Qty</th>
                                                <th style="padding: 4px 6px; border-right: 1px solid #e2e8f0;">Sales Rep</th>
                                                <th style="padding: 4px 6px; text-align: right; color: #4f46e5;">SO Total Value (฿)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                        """
                        
                        for tx in item_data['txs']:
                            nested_html += f"""
                            <tr style="border-bottom: 1px solid #f1f5f9; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor='#eef2ff'" onmouseout="this.style.backgroundColor='white'">
                                <td style="padding: 4px 6px; border-right: 1px solid #f1f5f9; text-align: center;">{tx['date']}</td>
                                <td style="padding: 4px 6px; border-right: 1px solid #f1f5f9; font-family: monospace; font-weight: bold; color: #4f46e5;">{tx['so']}</td>
                                <td style="padding: 4px 6px; border-right: 1px solid #f1f5f9; font-family: monospace; color: #3b82f6;">{tx['quote']}</td>
                                <td style="padding: 4px 6px; border-right: 1px solid #f1f5f9; text-align: center; font-weight: bold;">{tx['qty']}</td>
                                <td style="padding: 4px 6px; border-right: 1px solid #f1f5f9;">{tx['rep']}</td>
                                <td style="padding: 4px 6px; text-align: right; font-weight: bold;">{safe_fmt(tx['val'])}</td>
                            </tr>
                            """
                            
                        nested_html += "</tbody></table></div></td></tr>"
                    nested_html += "</tbody></table></div></div>"
                
                ind_val = c['ind']
                ind_badge = f'<span style="background-color: #f3f4f6; color: #4b5563; padding: 2px 6px; border-radius: 4px; border: 1px solid #e5e7eb; font-size: 10px; font-weight: bold;">{ind_val}</span>' if ind_val != "Unknown" else '<span style="color: #9ca3af;">-</span>'
                last_date_str = format_th_date(c['lastDate'])
                safe_c_name = escape_html(c['name'])
                
                # =========================================================
                # 🔥 ป้องกันขั้นสุด: ส่งค่าผ่าน Data Attributes (Robust Design)
                # =========================================================
                safe_prod_mix = escape_html(json.dumps(prod_mix))
                safe_hist_text = escape_html(hist_text).replace('\n', '&#10;')
                safe_ltv = str(c['totalVal'])
                safe_so_count = str(c['soCount'])
                
                safe_attr_cust = escape_html(c['name'])
                safe_attr_ind = escape_html(ind_val)
                safe_attr_last_rep = escape_html(c['lastRep'])
                
                # ปุ่ม AI วิเคราะห์ (พร้อมคำสั่งกันคลิกทะลุ event.stopPropagation())
                btn_html = f'''<button 
                    data-cust="{safe_attr_cust}" 
                    data-ind="{safe_attr_ind}" 
                    data-last-rep="{safe_attr_last_rep}"
                    data-ltv="{safe_ltv}"
                    data-so-count="{safe_so_count}"
                    data-prod-mix="{safe_prod_mix}"
                    data-hist-text="{safe_hist_text}"
                    onclick="event.stopPropagation(); executeAiAnalysis(this);" 
                    style="background-color: #eab308; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-family: 'Sarabun', sans-serif; font-weight: bold; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.2s ease; display: inline-flex; align-items: center; justify-content: center; width: 100%; gap: 6px;"
                    onmouseover="this.style.backgroundColor='#ca8a04'; this.style.transform='scale(1.03)';" 
                    onmouseout="this.style.backgroundColor='#eab308'; this.style.transform='scale(1)';">
                    <i class="fa-solid fa-robot"></i> <span>AI วิเคราะห์</span>
                </button>'''
                
                # หั่น String ในตารางหลักประวัติลูกค้า
                hist_parts.append(f'<tr style="border-bottom: 1px solid #e2e8f0; cursor: pointer; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#eef2ff\'" onmouseout="this.style.backgroundColor=\'white\'" onclick="toggleDetail(\'{rid}\', this)">')
                hist_parts.append(f'<td style="padding: 6px 10px; text-align: center;"><div class="rotate-icon" style="transition: transform 0.2s; color: #9ca3af;">▼</div></td>')
                hist_parts.append(f'<td style="padding: 6px 10px; font-weight: 500; color: #1f2937; font-size: 13px;">{safe_c_name}</td>')
                hist_parts.append(f'<td style="padding: 6px 10px; text-align: center;">{ind_badge}</td>')
                hist_parts.append(f'<td style="padding: 6px 10px; text-align: center; font-weight: bold; color: #4f46e5; font-size: 13px; background-color: #eef2ff;">{c["soCount"]}</td>')
                hist_parts.append(f'<td style="padding: 6px 10px; text-align: right; font-weight: bold; color: #3730a3; font-size: 13px;">{safe_fmt(c["totalVal"])}</td>')
                hist_parts.append(f'<td style="padding: 6px 10px; text-align: center; color: #6b7280; font-size: 12px;">{last_date_str}</td>')
                hist_parts.append(f'<td style="padding: 6px 10px; color: #4b5563; font-size: 12px;">{c["lastRep"]}</td>')
                hist_parts.append(f'<td style="padding: 6px 10px; text-align: center; vertical-align: middle;" onclick="event.stopPropagation()">{btn_html}</td></tr>')
                
                hist_parts.append(f'<tr id="{rid}" class="detail-row" style="display: none; background-color: #f8fafc;"><td colspan="8" style="padding: 0; border-bottom: 2px solid #c7d2fe;"><div style="padding: 12px 16px; border-left: 4px solid #818cf8;"><h5 style="font-size: 13px; font-weight: bold; color: #312e81; margin-bottom: 12px; display: flex; align-items: center; margin-top: 0;"><span style="margin-right: 6px; font-size: 14px;">⏱️</span> ประวัติงานและการสั่งซื้อ (จัดกลุ่มตามรหัสสินค้า - Item Code)</h5>{nested_html}</div></td></tr>')
            
            hist_parts.append('</tbody></table></div>')
            
            # =========================================================
            # 🔥 BULLETPROOF JAVASCRIPT BLOCK (ฉีดเฉพาะสำหรับ Tab 7: AI วิเคราะห์ลูกค้าทั่วไป)
            # =========================================================
            bulletproof_js = """
            <script>
            // 1. Safe Storage Wrapper
            let memStore = {};
            function safeGetItem(key) { try { return localStorage.getItem(key) || memStore[key] || ""; } catch(e) { return memStore[key] || ""; } }
            function safeSetItem(key, val) { try { localStorage.setItem(key, val); } catch(e) {} memStore[key] = val; }
            function safeRemoveItem(key) { try { localStorage.removeItem(key); } catch(e) {} delete memStore[key]; }

            // 2. โหลด Chart.js ถ้ายังไม่มี
            function loadChartJsAndRender(labels, dataVals) {
                if (window.Chart) {
                    renderAiChart(labels, dataVals);
                } else {
                    const script = document.createElement('script');
                    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
                    script.onload = () => renderAiChart(labels, dataVals);
                    document.head.appendChild(script);
                }
            }

            function renderAiChart(labels, dataVals) {
                const ctx = document.getElementById('aiCustomerChart');
                if(!ctx) return;
                if(window.aiCustChart) window.aiCustChart.destroy();
                window.aiCustChart = new Chart(ctx.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: dataVals,
                            backgroundColor: ['#3b82f6', '#0ea5e9', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#64748b'],
                            borderWidth: 2, borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false, cutout: '65%',
                        plugins: {
                            legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10, family: 'Sarabun' } } },
                            tooltip: { callbacks: { label: function(context) { return ' ' + context.label + ': ' + context.raw.toLocaleString() + ' ฿'; } } }
                        }
                    }
                });
            }

            // 3. ดักจับการคลิกอย่างปลอดภัย
            window.executeAiAnalysis = function(btn) {
                const cust = btn.getAttribute('data-cust') || 'Unknown';
                const ind = btn.getAttribute('data-ind') || 'Unknown';
                const lastRep = btn.getAttribute('data-last-rep') || 'Unknown';
                const ltv = btn.getAttribute('data-ltv') || '0';
                const soCount = btn.getAttribute('data-so-count') || '0';
                const prodMixStr = btn.getAttribute('data-prod-mix') || '{}';
                const histText = btn.getAttribute('data-hist-text') || '';
                
                // Visual Feedback (แสดงสถานะกำลังโหลด)
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>กำลังเตรียมระบบ...</span>';
                btn.style.opacity = '0.8';
                btn.disabled = true;
                
                // สั่งการให้ AI ทำงาน (เพิ่มดีเลย์เล็กน้อยให้ UI ขยับ)
                setTimeout(() => {
                    robustTriggerAI(cust, ind, lastRep, ltv, soCount, prodMixStr, histText);
                    btn.innerHTML = originalHtml;
                    btn.style.opacity = '1';
                    btn.disabled = false;
                }, 100);
            };

            window.saveLocalKeyAndRun = function() {
                const val = document.getElementById('tempApiKey').value.trim();
                if(val) {
                    safeSetItem('local_gemini_key', val);
                    robustTriggerAI(currentAiArgs.custName, currentAiArgs.ind, currentAiArgs.lastRep, currentAiArgs.ltv, currentAiArgs.soCount, currentAiArgs.prodMixStr, currentAiArgs.histText);
                } else {
                    alert('⚠️ กรุณาวาง API Key ก่อนกดบันทึก');
                }
            };

            window.resetLocalKey = function() {
                safeRemoveItem('local_gemini_key');
                alert('✅ ล้าง API Key ออกจากระบบเรียบร้อยแล้ว');
                const modal = document.getElementById('aiModal');
                if(modal) modal.style.display = 'none';
            };

            // 4. The Main Robust AI Logic (ฟังก์ชั่นหลักวิเคราะห์ลูกค้าปัจจุบัน)
            window.robustTriggerAI = async function(custName, ind, lastRep, ltv, soCount, prodMixStr, histText) {
                currentAiArgs = { custName, ind, lastRep, ltv, soCount, prodMixStr, histText };
                let activeKey = safeGetItem('local_gemini_key');
                
                const modal = document.getElementById('aiModal');
                const body = document.getElementById('aiModalBody');
                
                if (!modal || !body) return;
                modal.style.display = 'flex';
                
                if (!activeKey) {
                    if(typeof showKeyInputScreen === "function") showKeyInputScreen(body);
                    return;
                }

                // แปลง Product Mix JSON
                let prodMix = {};
                try {
                    const unescaped = prodMixStr.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
                    prodMix = JSON.parse(unescaped);
                } catch(e) { console.error("Parse JSON error", e); }
                let labels = Object.keys(prodMix);
                let dataVals = Object.values(prodMix);

                // สร้าง Layout UI (Theme สีฟ้า สำหรับ Tab 7)
                body.innerHTML = `
                    <div style="font-family: 'Sarabun', sans-serif;">
                        <div style="display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); gap: 16px; margin-bottom: 24px;">
                            <div style="background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); border-radius: 12px; padding: 20px; color: white; position: relative; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <i class="fa-solid fa-address-card" style="position: absolute; right: -20px; bottom: -20px; font-size: 100px; color: rgba(255,255,255,0.1); transform: rotate(-10deg);"></i>
                                <div style="display: inline-block; padding: 2px 8px; background: rgba(59, 130, 246, 0.5); border-radius: 4px; font-size: 10px; text-transform: uppercase; font-weight: bold; margin-bottom: 8px; border: 1px solid rgba(96, 165, 250, 0.5);">Customer Profile</div>
                                <h2 style="font-size: 24px; font-weight: bold; margin: 0 0 4px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${custName}</h2>
                                <p style="color: #e0f2fe; font-size: 13px; margin: 0 0 16px 0;"><i class="fa-solid fa-user-tie" style="margin-right: 6px;"></i>ดูแลโดย: ${lastRep}</p>
                                
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; border-top: 1px solid rgba(59, 130, 246, 0.5); padding-top: 16px;">
                                    <div>
                                        <div style="font-size: 10px; color: #bae6fd; text-transform: uppercase; margin-bottom: 2px;">Historical LTV</div>
                                        <div style="font-size: 24px; font-weight: 900; color: #fef08a;">${Number(ltv).toLocaleString('en-US')} <span style="font-size: 14px; font-weight: normal;">THB</span></div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10px; color: #bae6fd; text-transform: uppercase; margin-bottom: 2px;">Total Transactions</div>
                                        <div style="font-size: 24px; font-weight: 900; color: white;">${soCount} <span style="font-size: 14px; font-weight: normal; color: #e0f2fe;">SOs</span></div>
                                    </div>
                                </div>
                            </div>
                            <div style="background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e7ff; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                <h3 style="font-size: 11px; font-weight: bold; color: #6b7280; text-transform: uppercase; width: 100%; text-align: left; margin: 0 0 8px 0;"><i class="fa-solid fa-chart-pie" style="color: #3b82f6; margin-right: 6px;"></i>สัดส่วนผลิตภัณฑ์ (Product Mix)</h3>
                                <div style="position: relative; width: 100%; height: 150px;">
                                    <canvas id="aiCustomerChart"></canvas>
                                </div>
                            </div>
                        </div>
                        
                        <div id="aiPlanContent" style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #f3f4f6; font-family: 'Sarabun', sans-serif;">
                            <div style="text-align: center; padding: 40px 0;">
                                <i class="fa-solid fa-robot fa-bounce" style="font-size: 40px; color: #3b82f6; margin-bottom: 16px;"></i>
                                <p style="color: #6b7280; font-size: 14px; font-weight: bold;">AI กำลังวิเคราะห์ข้อมูลเชิงลึกและร่างแผนการเข้าทำ (Account Plan)...</p>
                            </div>
                        </div>
                    </div>
                `;

                // สั่งวาดกราฟวงกลม
                loadChartJsAndRender(labels, dataVals);

                // ส่งคำสั่ง AI แบบเดียวกับ Tab 8 แต่ปรับให้เป็นการเข้าพบลูกค้าปัจจุบัน (Account Planning)
                const sysPrompt = `คุณคือ "Sales Strategy AI" ผู้ช่วยผู้จัดการฝ่ายขาย B2B ที่เก่งที่สุด ให้คำแนะนำที่ตรงประเด็นและใช้งานได้จริง
อ้างอิงข้อมูลผลิตภัณฑ์ของบริษัท www.siamrajpump.com มีดังนี้:
- DP (Durco), PL (Peerless), GP (ITT-Goulds): กลุ่ม "Industrial Process Pump (API & ANSI Standard)" อดีตเราเคยเป็นตัวแทน DP และ PL ปัจจุบันเราเป็นตัวแทนจำหน่าย GP (หากพบว่าลูกค้าเคยซื้อ DP หรือ PL ให้เสนอแผนนำ GP ไปทดแทน)
- WF: Wrightflow Technology Lobe pump (ปัจจุบันเปลี่ยนชื่อเป็น Viking Hygienic Lobe pump แต่ยังคงใช้รหัส WF และแยกสายผลิตภัณฑ์กับ VK โดยสิ้นเชิง)
- VK: VIKING (Gear Pump)
- WR หมายถึง SandPiper Pump, Diaphragm AODD
- CG: COGNITO (EODD)
- CK: CORKEN (COMPRESSOR)
- LC: LC METER (PD Meter)
- GL: GOULDS WATER
- KB: KSB PUMP & VALVE
- TN: POMPETRAVAINI
- IM: IMO (Multi screw)
- SP: SEEPEX (Single screw)
- HV: HOWDEN TURBO
- SE: SES & KWANGSHIN
- VP: PIGGING SYSTEM

ข้อกำหนด:
- ห้ามเกริ่นนำ ให้เข้าเรื่องเลย
- ใช้สัญลักษณ์ Emoji หน้าหัวข้อหลัก
- ใช้ Bold เน้นข้อความ
- ใช้ Bullet points`;

                const unescapedHist = histText.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
                const prompt = `ลูกค้ารายนี้ชื่อ "${custName}"
อุตสาหกรรม: ${ind}
ประวัติย้อนหลัง (ตัวอย่าง 20 รายการล่าสุด):
${unescapedHist}

วิเคราะห์ข้อมูลและจัดทำ "แผนการเข้าทำ (Account Plan)" 4 กลยุทธ์ตามโครงสร้างนี้:
1. 🏢 ข้อมูลนิติบุคคลและภาพรวมธุรกิจ (วิเคราะห์จากชื่อและอุตสาหกรรมว่าลักษณะธุรกิจหลักคืออะไร และใช้ปั๊มทำอะไร)
2. ⚙️ วิเคราะห์กระบวนการผลิตและของเหลวที่ใช้ (ประเมินว่ากระบวนการผลิตของลูกค้าคืออะไร และมีโอกาสซ่อมบำรุงส่วนไหน)
3. 💡 โอกาสในการต่อยอด (Cross-sell / Up-sell) (วิเคราะห์จากประวัติการซื้อ ว่าควรนำเสนอสินค้าใดเพิ่มเติม)
4. 🎯 แผนปฏิบัติการ (Action Plan) สำหรับทีมขาย
สรุปจบด้วย Action Plan 3 Step: 
- Step 1 (เข้าถึง): วิธีเข้าหาลูกค้า
- Step 2 (นำเสนอ): สิ่งที่จะนำไปเสนอ
- Step 3 (ปิดจบ): กลยุทธ์กระตุ้นการตัดสินใจ`;

                try {
                    let targetModel = "gemini-1.5-flash"; 
                    try {
                        const mRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${activeKey}`);
                        if (mRes.ok) {
                            const mData = await mRes.json();
                            const vModels = mData.models.filter(m => m.supportedGenerationMethods && m.supportedGenerationMethods.includes("generateContent"));
                            if(vModels.find(m => m.name.includes("gemini-1.5-flash"))) targetModel = "gemini-1.5-flash";
                            else if(vModels.find(m => m.name.includes("gemini-1.5-pro"))) targetModel = "gemini-1.5-pro";
                            else if(vModels.length > 0) targetModel = vModels[0].name.replace('models/', '');
                        }
                    } catch(e) { console.warn("Model auto-discovery skipped due to network/cors."); }

                    const payload = { contents: [{ parts: [{ text: `[คำสั่งพิเศษสำหรับคุณ: ${sysPrompt}]\\n\\nข้อมูลที่ต้องวิเคราะห์:\\n${prompt}` }] }] };
                    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:generateContent?key=${activeKey}`;

                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    
                    const data = await response.json();

                    if (!response.ok) throw new Error(data.error?.message || `HTTP ${response.status} Error`);
                    
                    const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
                    if(!text) throw new Error("API ประมวลผลสำเร็จ แต่ไม่มีเนื้อหาตอบกลับ (Empty Content)");
                    
                    const aiContainer = document.getElementById('aiPlanContent');
                    if (aiContainer) {
                        try {
                            if (window.marked) {
                                aiContainer.innerHTML = marked.parse(text);
                            } else {
                                // เปลี่ยนสีหัวข้อให้เป็นโทนฟ้าเข้ากับหน้าต่าง
                                let html = text
                                    .replace(/^### (.*$)/gim, '<h3 style="background-color: #e0f2fe; padding: 4px 10px; border-radius: 4px; border-left: 3px solid #0ea5e9; font-size: 15px; font-weight: bold; color: #0369a1; margin-top: 20px; margin-bottom: 8px;">$1</h3>')
                                    .replace(/^## (.*$)/gim, '<h2 style="font-weight: bold; font-size: 18px; margin-top: 24px; margin-bottom: 12px; color: #1e40af;">$1</h2>')
                                    .replace(/^# (.*$)/gim, '<h1 style="font-weight: bold; font-size: 22px; margin-bottom: 12px; color: #1e3a8a; border-bottom: 2px solid #e0f2fe; padding-bottom: 8px;">$1</h1>')
                                    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: #111827; font-weight: bold; background-color: rgba(254, 240, 138, 0.25); padding: 0 4px; border-radius: 3px; border-bottom: 1px solid #fde047;">$1</strong>')
                                    .replace(/\\*(.*?)\\*/g, '<em style="color: #2563eb; font-style: normal; font-weight: bold;">$1</em>');
                                
                                aiContainer.innerHTML = `<div style="padding: 8px;"><div style="margin-bottom: 16px; line-height: 1.6; color: #4b5563; font-size: 14px; white-space: pre-wrap;">${html}</div></div>`;
                            }
                        } catch(e) {
                            aiContainer.innerHTML = `<div style="white-space: pre-wrap; font-size: 14px;">${text}</div>`;
                        }
                    }
                    
                } catch (err) {
                    let errorMsg = err.message;
                    let showResetBtn = false;
                    
                    if (errorMsg.includes("API_KEY_INVALID") || errorMsg.includes("API key not valid") || errorMsg.includes("400")) {
                        errorMsg = "API Key ไม่ถูกต้อง (Invalid API Key) กรุณาตรวจสอบว่าคัดลอกมาครบถ้วน";
                        showResetBtn = true;
                    } else if (errorMsg.includes("403") || errorMsg.includes("permission") || errorMsg.includes("unregistered")) {
                        errorMsg = "API Key นี้ไม่มีสิทธิ์เข้าถึง (Permission Denied) ระบบอาจถูกระงับ";
                        showResetBtn = true;
                    } else if (errorMsg.includes("429") || errorMsg.includes("quota")) {
                        errorMsg = "โควต้าการใช้งาน AI ของคุณถูกใช้จนเต็ม (Quota Exceeded) กรุณารอสักครู่";
                    }
                    
                    const aiContainer = document.getElementById('aiPlanContent');
                    if (aiContainer) {
                        aiContainer.innerHTML = `
                            <div style="text-align:center; padding:40px 20px; color:#b91c1c; background-color:#fef2f2; border-radius:8px;">
                                <i class="fa-solid fa-triangle-exclamation" style="font-size:50px; margin-bottom:16px; color:#ef4444;"></i>
                                <h3 style="color:#991b1b; margin-bottom:8px; font-weight: bold;">พบข้อผิดพลาดจากระบบ AI</h3>
                                <p style="font-size:13px; margin-bottom:24px; color:#6b7280; font-family:monospace;">${errorMsg}</p>
                                <button onclick="resetLocalKey()" style="background:#ef4444; color:white; padding:8px 16px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; font-size:13px;"><i class="fa-solid fa-rotate-right" style="margin-right:6px;"></i> ${showResetBtn ? 'ล้าง API Key แล้วตั้งค่าใหม่' : 'ล้าง API Key ในระบบ'}</button>
                            </div>
                        `;
                    }
                }
            };
            </script>
            """
            hist_parts.append(bulletproof_js)
            
            html_with_ai = f"{COMMON_HTML_HEAD}<body>{''.join(hist_parts)}</body>"
            components.html(html_with_ai, height=800, scrolling=True)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการประมวลผล (Tab 7): {str(e)}")

# ------------------------------------------
# TAB 8: ลูกค้าที่ห่างหาย (>5 ปี)
# ------------------------------------------
with tab8:
    try:
        import json
        ch_inactive = {}
        for d in df_so_all.itertuples(index=False):
            if selected_group != "All" and getattr(d, 'Group', 'Others') != selected_group:
                continue
            c_name = str(getattr(d, 'Customer', 'Unknown'))
            if c_name not in ch_inactive:
                ch_inactive[c_name] = {
                    'name': c_name,
                    'totalVal': 0.0,
                    'history': [],
                    'lastDate': pd.Timestamp('1900-01-01'),
                    'lastRep': '',
                    'lastProd': '',
                    'ind': str(getattr(d, 'Industry', 'Unknown')) if pd.notna(getattr(d, 'Industry', 'Unknown')) else 'Unknown'
                }
            val = float(getattr(d, 'Actual', 0)) if pd.notna(getattr(d, 'Actual', 0)) else 0.0
            ch_inactive[c_name]['totalVal'] += val
            
            h_record = {
                'Year': getattr(d, 'Year', '-'), 
                'Month': getattr(d, 'Month', 0), 
                'SONumber': getattr(d, 'SONumber', '-'), 
                'Product': getattr(d, 'Product', '-'), 
                'Industry': getattr(d, 'Industry', '-'), 
                'SalesRep': getattr(d, 'SalesRep', '-'), 
                'Actual': val, 
                'QuotationNo': getattr(d, 'QuotationNo', '-')
            }
            ch_inactive[c_name]['history'].append(h_record)

            so_date = getattr(d, 'SODate', pd.NaT)
            if pd.notna(so_date) and so_date > ch_inactive[c_name]['lastDate']:
                ch_inactive[c_name]['lastDate'] = so_date
                ch_inactive[c_name]['lastRep'] = str(getattr(d, 'SalesRep', '-'))
                ch_inactive[c_name]['lastProd'] = str(getattr(d, 'Product', '-'))

        today = pd.Timestamp.now()
        inactive_list = []
        for c_name, data in ch_inactive.items():
            if data['lastDate'] > pd.Timestamp('1900-01-01'):
                years_diff = (today - data['lastDate']).days / 365.25
                if years_diff > 5.0:
                    data['years'] = float(years_diff)
                    inactive_list.append(data)
                    
        all_inactive_inds = sorted(list(set(str(c['ind']) for c in inactive_list)))
        all_inactive_reps = sorted(list(set(str(c['lastRep']) for c in inactive_list if pd.notna(c['lastRep']))))

        col_left, col_right = st.columns([7.5, 2.5])
        
        with col_right:
            csv_buffer = io.StringIO()
            csv_buffer.write("\uFEFFCustomer Name,Last Purchase Date,Inactive Years,Historical LTV,Last Sales Rep,Last Product,Industry (INDS)\n")
            
            export_list = sorted(inactive_list, key=lambda x: x['totalVal'], reverse=True)
            for c in export_list:
                safe_name_csv = str(c['name']).replace('"', '""')
                yrs = float(c.get("years", 0.0))
                tv = float(c.get("totalVal", 0.0))
                csv_buffer.write(f'"{safe_name_csv}","{format_th_date(c["lastDate"])}",{yrs:.1f},{tv},"{c["lastRep"]}","{c["lastProd"]}","{c["ind"]}"\n')
                
            st.download_button(
                label="📥 Export มอบหมายงาน",
                data=csv_buffer.getvalue().encode('utf-8'),
                file_name=f"Winback_Target_Group_{selected_group}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            cur_inact_ind = st.selectbox("🏭 อุตสาหกรรม:", ["All"] + all_inactive_inds, key="inact_ind_tab6")
            cur_inact_rep = st.selectbox("👤 พนักงานขาย:", ["All"] + all_inactive_reps, key="inact_rep_tab6")

        filtered_inactive = inactive_list
        if cur_inact_ind != 'All':
            filtered_inactive = [c for c in filtered_inactive if c['ind'] == cur_inact_ind]
        if cur_inact_rep != 'All':
            filtered_inactive = [c for c in filtered_inactive if c['lastRep'] == cur_inact_rep]

        total_inactive = len(filtered_inactive)
        total_ltv = sum(c['totalVal'] for c in filtered_inactive)
        avg_gap = sum(c['years'] for c in filtered_inactive) / total_inactive if total_inactive > 0 else 0.0

        with col_left:
            st.markdown("""
                <div style="border-left: 4px solid #ef4444; background-color: #fef2f2; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); display: flex; align-items: center; flex-wrap: wrap; gap: 8px; font-family: 'Sarabun', sans-serif;">
                    <h2 style="color: #991b1b; font-size: 18px; margin: 0; font-family: 'Sarabun', sans-serif;">🚨 Inactive Customer Recovery Logic (>5 Years)</h2>
                    <span style="color: #b91c1c; font-size: 13px; font-family: 'Sarabun', sans-serif;">| ระบุลูกค้าที่เงียบหายไปนานกว่า 5.0 ปี เพื่อให้ทีมขายกำหนดกลยุทธ์เข้าติดต่อซ้ำ</span>
                </div>
            """, unsafe_allow_html=True)
            
            k1, k2, k3 = st.columns(3)
            k1.markdown(f'<div class="metric-card" style="border-left: 4px solid #ef4444; padding: 20px;"><div style="color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 4px; text-transform: uppercase;">INACTIVE ACCOUNTS (>5Y)</div><div style="color: #dc2626; font-size: 11px; font-weight: 600; margin-bottom: 12px; background-color: #fee2e2; border-radius: 4px; padding: 3px 8px; display: inline-block;">{sub_group_only}</div><div style="font-size: 28px; font-weight: 800; color: #b91c1c;">{safe_fmt(total_inactive)} <span style="font-size:14px; font-weight: 600; color:#94a3b8;">ราย</span></div></div>', unsafe_allow_html=True)
            k2.markdown(f'<div class="metric-card" style="border-left: 4px solid #f97316; padding: 20px;"><div style="color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 4px; text-transform: uppercase;">HISTORICAL LTV POT.</div><div style="color: #ea580c; font-size: 11px; font-weight: 600; margin-bottom: 12px; background-color: #ffedd5; border-radius: 4px; padding: 3px 8px; display: inline-block;">{sub_group_only}</div><div style="font-size: 28px; font-weight: 800; color: #c2410c;">{safe_fmt(total_ltv)} <span style="font-size:14px; font-weight: 600; color:#94a3b8;">฿</span></div></div>', unsafe_allow_html=True)
            k3.markdown(f'<div class="metric-card" style="border-left: 4px solid #6b7280; padding: 20px;"><div style="color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 4px; text-transform: uppercase;">AVG. GAP YRS</div><div style="color: #4b5563; font-size: 11px; font-weight: 600; margin-bottom: 12px; background-color: #f3f4f6; border-radius: 4px; padding: 3px 8px; display: inline-block;">{sub_group_only}</div><div style="font-size: 28px; font-weight: 800; color: #374151;">{safe_fmt(avg_gap, 1)} <span style="font-size:14px; font-weight: 600; color:#94a3b8;">Y</span></div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        st.markdown('<h3 style="font-weight: bold; color: #991b1b; font-size: 14px; margin-bottom: 8px; border-bottom: 1px solid #fecaca; padding-bottom: 4px; font-family: \'Sarabun\', sans-serif;">🚨 รายชื่อลูกค้าที่ห่างหาย (>5 ปี)</h3>', unsafe_allow_html=True)

        if not filtered_inactive:
            st.info("ไม่พบข้อมูลลูกค้าที่ห่างหายตามเงื่อนไขนี้")
        else:
            ia_parts = []
            ia_parts.append('<div style="border: 1px solid #fca5a5; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 1px 2px rgba(0,0,0,0.05); font-family: \'Sarabun\', sans-serif;"><table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;"><thead style="background-color: #fef2f2; color: #7f1d1d; font-weight: bold; text-transform: uppercase; font-size: 11px; border-bottom: 2px solid #fecaca;"><tr><th style="padding: 8px 10px; width: 30px; text-align: center;"></th><th style="padding: 8px 10px;">Customer Name</th><th style="padding: 8px 10px; text-align: center;">Last Purchase</th><th style="padding: 8px 10px; text-align: center;">Inactive Years</th><th style="padding: 8px 10px; text-align: right;">Historical LTV</th><th style="padding: 8px 10px;">Last Rep</th><th style="padding: 8px 10px;">Product</th><th style="padding: 8px 10px; text-align: center; width: 120px;">Action</th></tr></thead><tbody>')

            for i, c in enumerate(sorted(filtered_inactive, key=lambda x: x['totalVal'], reverse=True)):
                rid = f"inact-cust-{i}"
                safe_name = escape_html(c['name'])
                last_date_str = format_th_date(c['lastDate'])
                years_str = safe_fmt(c['years'], 1)

                sorted_h = sorted(c['history'], key=lambda x: (x['Year'], x['Month']), reverse=True)
                
                # =========================================================
                # 🔥 จัดเตรียมข้อมูลสำหรับการวิเคราะห์ AI ขั้นสูง
                # =========================================================
                prod_mix = {}
                hist_text = ""
                for idx, h in enumerate(sorted_h):
                    p = str(h.get('Product', 'Unknown'))
                    v = float(h.get('Actual', 0.0))
                    prod_mix[p] = prod_mix.get(p, 0.0) + v
                    # ดึงประวัติ 20 บรรทัดแรกไปให้ AI (กันข้อมูลล้น)
                    if idx < 20:
                        hist_text += f"- {int(h.get('Month', 0))}/{h.get('Year', '-')} | {p} | {v:,.0f} THB\n"
                
                safe_prod_mix = escape_html(json.dumps(prod_mix))
                # เข้ารหัส \n เป็น &#10; เพื่อป้องกันปัญหา Syntax ใน Attribute
                safe_hist_text = escape_html(hist_text).replace('\n', '&#10;')
                safe_ltv = str(c['totalVal'])
                safe_so_count = str(len(c['history']))
                safe_last_rep = escape_html(c['lastRep'])
                safe_ind = escape_html(c['ind'])
                
                # ใส่ onclick="event.stopPropagation(); executeAiAnalysis(this);" ที่ตัวปุ่มเลย ป้องกันการคลี่หน้าต่าง
                btn_html = f'''<button 
                    data-cust="{safe_name}" 
                    data-ind="{safe_ind}" 
                    data-last-rep="{safe_last_rep}"
                    data-ltv="{safe_ltv}"
                    data-so-count="{safe_so_count}"
                    data-prod-mix="{safe_prod_mix}"
                    data-hist-text="{safe_hist_text}"
                    onclick="event.stopPropagation(); executeAiAnalysis(this);" 
                    style="background-color: #ef4444; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-family: 'Sarabun', sans-serif; font-weight: bold; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.2s ease; display: inline-flex; align-items: center; justify-content: center; width: 100%; gap: 6px;"
                    onmouseover="this.style.backgroundColor='#b91c1c'; this.style.transform='scale(1.03)';" 
                    onmouseout="this.style.backgroundColor='#ef4444'; this.style.transform='scale(1)';">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> <span>แผนกู้คืน</span>
                </button>'''

                ia_parts.append(f'<tr style="border-bottom: 1px solid #fee2e2; cursor: pointer; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#fef2f2\'" onmouseout="this.style.backgroundColor=\'white\'" onclick="toggleDetail(\'{rid}\', this)">')
                ia_parts.append('<td style="padding: 6px 10px; text-align: center;"><div class="rotate-icon" style="transition: transform 0.2s; color: #9ca3af;">▼</div></td>')
                ia_parts.append(f'<td style="padding: 6px 10px; font-weight: 500; color: #374151; font-size: 13px;">{safe_name}</td>')
                ia_parts.append(f'<td style="padding: 6px 10px; text-align: center; color: #6b7280; font-size: 13px;">{last_date_str}</td>')
                ia_parts.append(f'<td style="padding: 6px 10px; text-align: center; font-weight: bold; color: #dc2626; background-color: #fef2f2; font-size: 13px;">{years_str}</td>')
                ia_parts.append(f'<td style="padding: 6px 10px; text-align: right; font-weight: bold; color: #4338ca; font-size: 13px;">{safe_fmt(c["totalVal"])}</td>')
                ia_parts.append(f'<td style="padding: 6px 10px; color: #4b5563; font-size: 13px;">{safe_last_rep}</td>')
                ia_parts.append(f'<td style="padding: 6px 10px; color: #4b5563; font-size: 13px;">{escape_html(c["lastProd"])}</td>')
                ia_parts.append(f'<td style="padding: 6px 10px; text-align: center; vertical-align: middle;" onclick="event.stopPropagation()">{btn_html}</td></tr>')

                nested_html = '<div style="padding: 12px 16px; border-left: 4px solid #fca5a5;"><h5 style="font-size: 13px; font-weight: bold; color: #7f1d1d; margin-bottom: 12px; margin-top: 0;"><i class="fa-solid fa-history" style="margin-right: 6px;"></i> Transaction History</h5><table style="width: 100%; border: 1px solid #e5e7eb; background-color: white; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); font-size: 11px;"><thead style="background-color: #f3f4f6; color: #4b5563; border-bottom: 1px solid #e5e7eb;"><tr><th style="padding: 4px 6px; border-right: 1px solid #e5e7eb; text-align: center;">Date</th><th style="padding: 4px 6px; border-right: 1px solid #e5e7eb;">SO / Job No.</th><th style="padding: 4px 6px; border-right: 1px solid #e5e7eb; color: #2563eb;">Quotation No.</th><th style="padding: 4px 6px; border-right: 1px solid #e5e7eb;">Product</th><th style="padding: 4px 6px; border-right: 1px solid #e5e7eb; color: #0d9488;">Industry (INDS)</th><th style="padding: 4px 6px; border-right: 1px solid #e5e7eb;">Sales Rep</th><th style="padding: 4px 6px; text-align: right;">Value</th></tr></thead><tbody>'

                for h in sorted_h:
                    q_no = str(h.get('QuotationNo', '-')).strip()
                    if q_no.lower() == 'nan' or not q_no: q_no = '-'
                    val_h = float(h['Actual']) if pd.notna(h['Actual']) else 0.0
                    
                    nested_html += f'<tr style="border-bottom: 1px solid #f3f4f6; transition: background-color 0.2s;" onmouseover="this.style.backgroundColor=\'#f9fafb\'" onmouseout="this.style.backgroundColor=\'white\'">'
                    nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #f3f4f6; text-align: center;">{int(h["Month"])}/{h["Year"]}</td>'
                    nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #f3f4f6; font-family: monospace; color: #4f46e5; font-weight: bold;">{escape_html(h["SONumber"])}</td>'
                    nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #f3f4f6; font-family: monospace; color: #3b82f6;">{escape_html(q_no)}</td>'
                    nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #f3f4f6; color: #4b5563;">{escape_html(h["Product"])}</td>'
                    nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #f3f4f6; color: #0d9488;">{escape_html(h["Industry"])}</td>'
                    nested_html += f'<td style="padding: 4px 6px; border-right: 1px solid #f3f4f6; color: #4b5563;">{escape_html(h["SalesRep"])}</td>'
                    nested_html += f'<td style="padding: 4px 6px; text-align: right; font-weight: bold; color: #374151;">{safe_fmt(val_h)}</td>'
                    nested_html += '</tr>'
                    
                nested_html += '</tbody></table></div>'

                ia_parts.append(f'<tr id="{rid}" class="detail-row" style="display: none; background-color: #f8fafc;"><td colspan="8" style="padding: 0; border-bottom: 2px solid #fecaca;">{nested_html}</td></tr>')

            ia_parts.append('</tbody></table></div>')
            
            # =========================================================
            # 🔥 BULLETPROOF JAVASCRIPT BLOCK (วิเคราะห์เชิงลึก + แก้ไข Syntax)
            # =========================================================
            bulletproof_js = """
            <script>
            let memStore = {};
            function safeGetItem(key) { try { return localStorage.getItem(key) || memStore[key] || ""; } catch(e) { return memStore[key] || ""; } }
            function safeSetItem(key, val) { try { localStorage.setItem(key, val); } catch(e) {} memStore[key] = val; }
            function safeRemoveItem(key) { try { localStorage.removeItem(key); } catch(e) {} delete memStore[key]; }

            function loadChartJsAndRender(labels, dataVals) {
                if (window.Chart) {
                    renderAiChart(labels, dataVals);
                } else {
                    const script = document.createElement('script');
                    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
                    script.onload = () => renderAiChart(labels, dataVals);
                    document.head.appendChild(script);
                }
            }

            function renderAiChart(labels, dataVals) {
                const ctx = document.getElementById('aiCustomerChart');
                if(!ctx) return;
                if(window.aiCustChart) window.aiCustChart.destroy();
                window.aiCustChart = new Chart(ctx.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: dataVals,
                            backgroundColor: ['#4f46e5', '#0ea5e9', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#64748b'],
                            borderWidth: 2, borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false, cutout: '65%',
                        plugins: {
                            legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10, family: 'Sarabun' } } },
                            tooltip: { callbacks: { label: function(context) { return ' ' + context.label + ': ' + context.raw.toLocaleString() + ' ฿'; } } }
                        }
                    }
                });
            }

            window.executeAiAnalysis = function(btn) {
                const cust = btn.getAttribute('data-cust') || 'Unknown';
                const ind = btn.getAttribute('data-ind') || 'Unknown';
                const lastRep = btn.getAttribute('data-last-rep') || 'Unknown';
                const ltv = btn.getAttribute('data-ltv') || '0';
                const soCount = btn.getAttribute('data-so-count') || '0';
                const prodMixStr = btn.getAttribute('data-prod-mix') || '{}';
                const histText = btn.getAttribute('data-hist-text') || '';
                
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>กำลังสืบค้นข้อมูล...</span>';
                btn.style.opacity = '0.8';
                btn.disabled = true;
                
                setTimeout(() => {
                    robustTriggerAI(cust, ind, lastRep, ltv, soCount, prodMixStr, histText);
                    btn.innerHTML = originalHtml;
                    btn.style.opacity = '1';
                    btn.disabled = false;
                }, 100);
            };

            window.saveLocalKeyAndRun = function() {
                const val = document.getElementById('tempApiKey').value.trim();
                if(val) {
                    safeSetItem('local_gemini_key', val);
                    robustTriggerAI(currentAiArgs.custName, currentAiArgs.ind, currentAiArgs.lastRep, currentAiArgs.ltv, currentAiArgs.soCount, currentAiArgs.prodMixStr, currentAiArgs.histText);
                } else {
                    alert('⚠️ กรุณาวาง API Key ก่อนกดบันทึก');
                }
            };

            window.resetLocalKey = function() {
                safeRemoveItem('local_gemini_key');
                alert('✅ ล้าง API Key ออกจากระบบเรียบร้อยแล้ว');
                const modal = document.getElementById('aiModal');
                if(modal) modal.style.display = 'none';
            };

            window.robustTriggerAI = async function(custName, ind, lastRep, ltv, soCount, prodMixStr, histText) {
                currentAiArgs = { custName, ind, lastRep, ltv, soCount, prodMixStr, histText };
                let activeKey = safeGetItem('local_gemini_key');
                
                const modal = document.getElementById('aiModal');
                const body = document.getElementById('aiModalBody');
                
                if (!modal || !body) return;
                modal.style.display = 'flex';
                
                if (!activeKey) {
                    if(typeof showKeyInputScreen === "function") showKeyInputScreen(body);
                    return;
                }

                let prodMix = {};
                try {
                    const unescaped = prodMixStr.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
                    prodMix = JSON.parse(unescaped);
                } catch(e) { console.error("Parse JSON error", e); }
                let labels = Object.keys(prodMix);
                let dataVals = Object.values(prodMix);

                body.innerHTML = `
                    <div style="font-family: 'Sarabun', sans-serif;">
                        <div style="display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); gap: 16px; margin-bottom: 24px;">
                            <div style="background: linear-gradient(135deg, #312e81 0%, #4338ca 100%); border-radius: 12px; padding: 20px; color: white; position: relative; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <i class="fa-solid fa-building-user" style="position: absolute; right: -20px; bottom: -20px; font-size: 100px; color: rgba(255,255,255,0.1); transform: rotate(-10deg);"></i>
                                <div style="display: inline-block; padding: 2px 8px; background: rgba(99, 102, 241, 0.5); border-radius: 4px; font-size: 10px; text-transform: uppercase; font-weight: bold; margin-bottom: 8px; border: 1px solid rgba(129, 140, 248, 0.5);">Customer Profile</div>
                                <h2 style="font-size: 24px; font-weight: bold; margin: 0 0 4px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${custName}</h2>
                                <p style="color: #c7d2fe; font-size: 13px; margin: 0 0 16px 0;"><i class="fa-solid fa-user-tie" style="margin-right: 6px;"></i>ล่าสุดดูแลโดย: ${lastRep}</p>
                                
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; border-top: 1px solid rgba(99, 102, 241, 0.5); padding-top: 16px;">
                                    <div>
                                        <div style="font-size: 10px; color: #a5b4fc; text-transform: uppercase; margin-bottom: 2px;">Historical LTV</div>
                                        <div style="font-size: 24px; font-weight: 900; color: #facc15;">${Number(ltv).toLocaleString('en-US')} <span style="font-size: 14px; font-weight: normal;">THB</span></div>
                                    </div>
                                    <div>
                                        <div style="font-size: 10px; color: #a5b4fc; text-transform: uppercase; margin-bottom: 2px;">Total Transactions</div>
                                        <div style="font-size: 24px; font-weight: 900; color: white;">${soCount} <span style="font-size: 14px; font-weight: normal; color: #c7d2fe;">SOs</span></div>
                                    </div>
                                </div>
                            </div>
                            <div style="background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e7ff; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                <h3 style="font-size: 11px; font-weight: bold; color: #6b7280; text-transform: uppercase; width: 100%; text-align: left; margin: 0 0 8px 0;"><i class="fa-solid fa-chart-pie" style="color: #818cf8; margin-right: 6px;"></i>สัดส่วนผลิตภัณฑ์ (Product Mix)</h3>
                                <div style="position: relative; width: 100%; height: 150px;">
                                    <canvas id="aiCustomerChart"></canvas>
                                </div>
                            </div>
                        </div>
                        
                        <div id="aiPlanContent" style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #f3f4f6; font-family: 'Sarabun', sans-serif;">
                            <div style="text-align: center; padding: 40px 0;">
                                <i class="fa-solid fa-robot fa-bounce" style="font-size: 40px; color: #818cf8; margin-bottom: 16px;"></i>
                                <p style="color: #6b7280; font-size: 14px; font-weight: bold;">AI กำลังวิเคราะห์ข้อมูลเชิงลึกและร่างแผนการเข้าทำ (Account Plan)...</p>
                            </div>
                        </div>
                    </div>
                `;

                loadChartJsAndRender(labels, dataVals);

                const sysPrompt = `คุณคือ "Sales Strategy AI" ผู้ช่วยผู้จัดการฝ่ายขาย B2B ที่เก่งที่สุด ให้คำแนะนำที่ตรงประเด็นและใช้งานได้จริง
อ้างอิงข้อมูลผลิตภัณฑ์ของบริษัท www.siamrajpump.com มีดังนี้:
- DP (Durco), PL (Peerless), GP (ITT-Goulds): กลุ่ม "Industrial Process Pump (API & ANSI Standard)" อดีตเราเคยเป็นตัวแทน DP และ PL ปัจจุบันเราเป็นตัวแทนจำหน่าย GP (หากพบว่าลูกค้าเคยซื้อ DP หรือ PL ให้เสนอแผนนำ GP ไปทดแทน)
- WF: Wrightflow Technology Lobe pump (ปัจจุบันเปลี่ยนชื่อเป็น Viking Hygienic Lobe pump แต่ยังคงใช้รหัส WF และแยกสายผลิตภัณฑ์กับ VK โดยสิ้นเชิง)
- VK: VIKING (Gear Pump)
- WR หมายถึง SandPiper Pump, Diaphragm AODD
- CG: COGNITO (EODD)
- CK: CORKEN (COMPRESSOR)
- LC: LC METER (PD Meter)
- GL: GOULDS WATER
- KB: KSB PUMP & VALVE
- TN: POMPETRAVAINI
- IM: IMO (Multi screw)
- SP: SEEPEX (Single screw)
- HV: HOWDEN TURBO
- SE: SES & KWANGSHIN
- VP: PIGGING SYSTEM

ข้อกำหนด:
- ห้ามเกริ่นนำ ให้เข้าเรื่องเลย
- ใช้สัญลักษณ์ Emoji หน้าหัวข้อหลัก
- ใช้ Bold เน้นข้อความ
- ใช้ Bullet points`;

                const unescapedHist = histText.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
                const prompt = `ลูกค้ารายนี้ชื่อ "${custName}"
อุตสาหกรรม: ${ind}
ประวัติย้อนหลัง (ตัวอย่าง 20 รายการล่าสุด):
${unescapedHist}

วิเคราะห์ข้อมูลและจัดทำ "แผนการเข้าทำ" 4 กลยุทธ์ตามโครงสร้างนี้:
1. 🔧 งานซ่อมบำรุงและอะไหล่ (วิเคราะห์จากอายุการใช้งานเครื่องจักรที่เกิน 5 ปี น่าจะต้องซื้ออะไหล่ตัวไหนไป Service หรือซ่อมบำรุง)
2. 🎯 เจาะช่องว่างสินค้า (Cross-Selling)
3. 🚀 ทดแทนของเดิม (Tech Upgrade)
4. 🚨 ระดับความเสี่ยง (Churn Risk)
สรุปจบด้วย Action Plan แบ่งเป็นเฟส ระบุผู้รับผิดชอบและกิจกรรมที่ชัดเจน`;

                try {
                    let targetModel = "gemini-1.5-flash"; 
                    try {
                        const mRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${activeKey}`);
                        if (mRes.ok) {
                            const mData = await mRes.json();
                            const vModels = mData.models.filter(m => m.supportedGenerationMethods && m.supportedGenerationMethods.includes("generateContent"));
                            if(vModels.find(m => m.name.includes("gemini-1.5-flash"))) targetModel = "gemini-1.5-flash";
                            else if(vModels.find(m => m.name.includes("gemini-1.5-pro"))) targetModel = "gemini-1.5-pro";
                            else if(vModels.length > 0) targetModel = vModels[0].name.replace('models/', '');
                        }
                    } catch(e) { console.warn("Model auto-discovery skipped"); }

                    const payload = { contents: [{ parts: [{ text: `[คำสั่งพิเศษสำหรับคุณ: ${sysPrompt}]\\n\\nข้อมูลที่ต้องวิเคราะห์:\\n${prompt}` }] }] };
                    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:generateContent?key=${activeKey}`;

                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.error?.message || `HTTP ${response.status} Error`);
                    
                    const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
                    if(!text) throw new Error("API ประมวลผลสำเร็จ แต่ไม่มีเนื้อหาตอบกลับ (Empty Content)");
                    
                    const aiContainer = document.getElementById('aiPlanContent');
                    if (aiContainer) {
                        try {
                            if (window.marked) {
                                aiContainer.innerHTML = marked.parse(text);
                            } else {
                                // 🔥 ถอดการตัดคำขึ้นบรรทัดใหม่ด้วย Regex ออก และเปลี่ยนมาใช้ white-space แทน เพื่อแก้ปัญหา Syntax Error 100%
                                let html = text
                                    .replace(/^### (.*$)/gim, '<h3 style="background-color: #e0e7ff; padding: 4px 10px; border-radius: 4px; border-left: 3px solid #4f46e5; font-size: 15px; font-weight: bold; color: #4338ca; margin-top: 20px; margin-bottom: 8px;">$1</h3>')
                                    .replace(/^## (.*$)/gim, '<h2 style="font-weight: bold; font-size: 18px; margin-top: 24px; margin-bottom: 12px; color: #3730a3;">$1</h2>')
                                    .replace(/^# (.*$)/gim, '<h1 style="font-weight: bold; font-size: 22px; margin-bottom: 12px; color: #1e3a8a; border-bottom: 2px solid #e0e7ff; padding-bottom: 8px;">$1</h1>')
                                    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: #111827; font-weight: bold; background-color: rgba(254, 240, 138, 0.25); padding: 0 4px; border-radius: 3px; border-bottom: 1px solid #fde047;">$1</strong>')
                                    .replace(/\\*(.*?)\\*/g, '<em style="color: #4f46e5; font-style: normal; font-weight: bold;">$1</em>');
                                
                                aiContainer.innerHTML = `<div style="padding: 8px;"><div style="margin-bottom: 16px; line-height: 1.6; color: #4b5563; font-size: 14px; white-space: pre-wrap;">${html}</div></div>`;
                            }
                        } catch(e) {
                            aiContainer.innerHTML = `<div style="white-space: pre-wrap; font-size: 14px;">${text}</div>`;
                        }
                    }
                } catch (err) {
                    let errorMsg = err.message;
                    let showResetBtn = false;
                    
                    if (errorMsg.includes("API_KEY_INVALID") || errorMsg.includes("API key not valid") || errorMsg.includes("400")) {
                        errorMsg = "API Key ไม่ถูกต้อง (Invalid API Key) กรุณาตรวจสอบว่าคัดลอกมาครบถ้วน";
                        showResetBtn = true;
                    } else if (errorMsg.includes("403") || errorMsg.includes("permission") || errorMsg.includes("unregistered")) {
                        errorMsg = "API Key นี้ไม่มีสิทธิ์เข้าถึง (Permission Denied) ระบบอาจถูกระงับ";
                        showResetBtn = true;
                    } else if (errorMsg.includes("429") || errorMsg.includes("quota")) {
                        errorMsg = "โควต้าการใช้งาน AI ของคุณถูกใช้จนเต็ม (Quota Exceeded) กรุณารอสักครู่";
                    }
                    
                    const aiContainer = document.getElementById('aiPlanContent');
                    if (aiContainer) {
                        aiContainer.innerHTML = `
                            <div style="text-align:center; padding:40px 20px; color:#b91c1c; background-color:#fef2f2; border-radius:8px;">
                                <i class="fa-solid fa-triangle-exclamation" style="font-size:50px; margin-bottom:16px; color:#ef4444;"></i>
                                <h3 style="color:#991b1b; margin-bottom:8px; font-weight: bold;">พบข้อผิดพลาดจากระบบ AI</h3>
                                <p style="font-size:13px; margin-bottom:24px; color:#6b7280; font-family:monospace;">${errorMsg}</p>
                                <button onclick="resetLocalKey()" style="background:#ef4444; color:white; padding:8px 16px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; font-size:13px;"><i class="fa-solid fa-rotate-right" style="margin-right:6px;"></i> ${showResetBtn ? 'ล้าง API Key แล้วตั้งค่าใหม่' : 'ล้าง API Key ในระบบ'}</button>
                            </div>
                        `;
                    }
                }
            };
            </script>
            """
            ia_parts.append(bulletproof_js)
            
            html_with_ai = f"{COMMON_HTML_HEAD}<body>{''.join(ia_parts)}</body>"
            components.html(html_with_ai, height=700, scrolling=True)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการประมวลผล (Tab 8): {str(e)}")

# Footer
st.markdown("---")
st.caption("พัฒนาโดย: ทีมพัฒนาระบบ | แหล่งข้อมูล: อัปเดตอัตโนมัติจาก Google Drive (Synchronized with HTML Logic) | Siamraj PLC.")