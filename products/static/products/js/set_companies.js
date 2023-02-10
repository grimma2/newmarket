function setListParam (listName) {
    let names = document.querySelector('input[name="' + listName + '"]:checked')
    let query = listName + '='

    for (index in names) {
        if (names.at(-1) === names[index]) {
            query = query + names[index].textContent
        } else {
            query = query + names[index].textContent + ','
        }
    }
}
