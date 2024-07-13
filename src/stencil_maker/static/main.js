// const download_button = document.getElementById("download-button");
//
// function download_btn_handler(event) {
//   const stencil = document.getElementById("stencil");
//   const tmp_a = document.createElement("a");
//   tmp_a.src = stencil.src;
//   document.body.appendChild(tmp_a);
//   tmp_a.click();
//   document.body.removeChild(tmp_a);
// }
//
// download_button.addEventListener("click", download_btn_handler);

// const result = document.getElementById("result");
//
// function img_context_handler(event) {
//   event.preventDefault();
//   alert("Usa el botón de descargar");
// }
//
// function callback(mutation_list, observer) {
//   for (const mutation of mutation_list) {
//     for (const node of mutation.addedNodes) {
//       if (node.tagName == "IMG") {
//         node.addEventListener("contextmenu", img_context_handler);
//       }
//     }
//   }
// }
//
// const config = { attributes: false, childList: true, subtree: false };
//
// const observer = new MutationObserver(callback);
//
// observer.observe(result, config);
//
// const initial_stencil = document.getElementById("stencil");
// initial_stencil.addEventListener("contextmenu", img_context_handler);
