function switchTab(tabId) {
    // Hide all panes
    const panes = document.querySelectorAll('.tab-pane');
    panes.forEach(pane => pane.classList.remove('active'));

    // Deactivate all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Activate selected pane and button
    const targetPane = document.getElementById(tabId);
    if (targetPane) {
        targetPane.classList.add('active');
    }

    const activeBtn = Array.from(buttons).find(btn => btn.getAttribute('onclick').includes(tabId));
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// Log status on load
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hệ thống Trí tuệ Nhân tạo Định lượng Tài chính PTIT đã sẵn sàng.");
});
