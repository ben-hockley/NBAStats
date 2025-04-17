document.getElementById('myNBAtoggle').addEventListener('click', function() {
    const dropdown = document.getElementById('myNBAdropdown');
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
});