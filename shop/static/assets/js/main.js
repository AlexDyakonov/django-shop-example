window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    const headerHeight = header.offsetHeight;
    const scrollTop = document.documentElement.scrollTop;
  
    if (scrollTop < headerHeight * 1.5){
      header.classList.remove('header-hidden')
    
    } else if (scrollTop > headerHeight * 1.5 && scrollTop < headerHeight * 7){
      header.classList.add('header-hidden');
    } if (scrollTop > headerHeight * 7){
      header.classList.remove('header-hidden');
    }
  });
  
  console.log("works!!!")