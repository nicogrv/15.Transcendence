
const rankBoard = document.getElementById("classement")
const classementLoader = document.getElementById("classementLoader")
function addPlayerInRankBoard(text) {
    let div = document.createElement("div")
    div.classList.add("classementUser")
    let p = document.createElement("p")
    p.innerText = text
    div.appendChild(p)
    rankBoard.appendChild(div)
    
}

fetch(`${window.location.origin}/api/user/getRanking`)
.then(response => {
    if (!response.ok) {throw new Error('La requête a échoué');} return response.json(); })
.then(data => {
    classementLoader.remove()
    if ("error" in data)
        return addPlayerInRankBoard(data.error)
    else if ("ok" in data) {
        for (elem in data.ok) 
            addPlayerInRankBoard(`${parseInt(elem)+1}. ${Object.keys(data.ok[elem])[0]} ${Object.values(data.ok[elem])[0]}`)
        return
    }
    else
        return addPlayerInRankBoard(data)
})