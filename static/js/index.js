  function toggleSidebar() {
    console.log('clicked');
    var sidebar = document.getElementById('sidebar');
    var sidebarIcon = document.getElementById('sidebarIcon'); // Assuming you have an icon with this id

    if (sidebar && sidebarIcon) {
        sidebar.classList.toggle('collapsed');
        
        // Toggle the icon based on the sidebar state
        if (sidebar.classList.contains('collapsed')) {
            // Sidebar is collapsed, show the open icon (e.g., a cross)
            sidebarIcon.innerHTML = '<i class="fa-solid fa-bars"></i>'; // Change this to the HTML entity or icon you want
        } else {
            // Sidebar is open, show the close icon (e.g., a hamburger menu)
            sidebarIcon.innerHTML = '<i class="fa-solid fa-xmark"></i>'; // Change this to the HTML entity or icon you want
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Function to scroll the chat container to the bottom
    function scrollToBottom() {
        var chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    scrollToBottom()
})