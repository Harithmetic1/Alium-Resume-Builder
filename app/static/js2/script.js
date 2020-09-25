const arrowOne = document.querySelector('#image-one');
const arrowTwo = document.querySelector('#image-two');
const arrowThree = document.querySelector('#image-three');



const displayList1 = () => {
    document.querySelector('#link-one').classList.toggle('not-seen');
}

const displayList2 = () => {
    document.querySelector('#link-two').classList.toggle('not-seen');
}

const displayList3 = () => {
    document.querySelector('#link-three').classList.toggle('not-seen');
}

arrowOne.addEventListener('click', displayList1);
arrowTwo.addEventListener('click', displayList2);
arrowThree.addEventListener('click', displayList3);