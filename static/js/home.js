// let searchBar = document.getElementById('searchBar');
// let errorMessage = document.getElementById('error-message');
let paragraph = document.getElementById('par');
let searchFirstName = document.getElementById('searchFirstName');
let searchLastName = document.getElementById('searchLastName');
paragraph.innerHTML = 'HIIIII';

// searchBar.addEventListener('keyup', function (event) {
//     if (event.keyCode == 13) {
//         event.preventDefault;
//         document.getElementById('btnSearch').click();
//     }
// });

// function handleErrors(response) {
//     if (!response.ok) {
//         errorMessage.innerText =
//             "Sorry, that breed isn't available at the moment";
//         for (let i = 0; i < list_items.length; i++) {
//             list_items[i].src =
//                 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
//         }
//     }
//     return response;
// }

// async function getDogs() {
//     if (errorMessage.innerText != '') {
//         errorMessage.innerText = '';
//     }
//     let input = searchBar.value;
//     input = input.replace(/\s/g, '');
//     let response = await fetch(
//         `https://dog.ceo/api/breed/${input}/images/random/9`
//     )
//         .then(handleErrors)
//         .then(function (res) {
//             return res.json();
//         })
//         .catch((res) =>
//             console.log(
//                 'Can’t access response. Blocked by browser. Error: ' + res
//             )
//         );
//     let images = response.message;

//     for (let i = 0; i < list_items.length; i++) {
//         list_items[i].src = images[i];
//     }
//     console.log(list_items);
// }
