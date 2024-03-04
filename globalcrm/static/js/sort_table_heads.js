const tableHeaders = document.querySelectorAll('th[data-sort]');

tableHeaders.forEach(header => {
    header.addEventListener('click', () => {
        const sortField = header.getAttribute('data-sort');
        const currentUrl = window.location.href;
        const separator = currentUrl.includes('?') ? '&' : '?';

        window.location.href = `${currentUrl}${separator}sort_by=${sortField}`;
    });
});