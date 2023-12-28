
// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

//Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;




function toast(durantion, delay) {
  const btnCloses = document.querySelectorAll('.btn-close')
  if (btnCloses) {
    
    btnCloses.forEach(btnClose => {
      const autoRemove = setTimeout(() => {
        btnClose.parentElement.remove()
      }, durantion + delay + 100)
      btnClose.onclick = () => {
        btnClose.parentElement.remove()
        clearTimeout(autoRemove)
      }
    })
    
  }
}
// 
toast(2000, 3000)


function btnPages() {
  const btns = document.querySelectorAll('.btn__page')
  if (btns) {
    btns.forEach(btn => {
      const btnPage = document.querySelector('.btn__page.active')
      btnPage.classList.remove('active')
      btn.classList.add('active')
    })
  }
}

