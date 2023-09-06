window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    const headerHeight = header.offsetHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
    if (scrollTop < headerHeight * 2){
      header.classList.remove('header-hidden')
      header.classList.remove('header-sticky')
    } else if (scrollTop > headerHeight * 2 && scrollTop < headerHeight * 3){
      header.classList.add('header-hidden');
    } if (scrollTop > headerHeight * 3){
      header.classList.remove('header-hidden');
      header.classList.add('header-sticky')
    }
  });
  