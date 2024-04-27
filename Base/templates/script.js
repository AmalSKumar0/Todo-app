const inputBox= document.getElementById("input-box");
const listContainer=document.getElementById("list-pending-container");
const listContainerComp=document.getElementById("list-completed-container");
const pendingPara=document.querySelector("#pending");
const completePara=document.querySelector("#complete");
const h1=document.querySelector("h2");
// const listConatainer=document.querySelector(".listConatainer");
let count=0;
let compcount=0;

let bigData = { count: 0,compcount: 0,pendingTask: '',completeTask: '',ListName:' ' };

let dis=document.createElement("span");
dis.innerHTML= `${compcount}/${compcount+count} completed`;
h1.appendChild(dis);
dis.innerHTML= `${compcount}/${compcount+count} completed`;
h1.appendChild(dis);
dis.setAttribute("id","count");

function addTask(){
    if(inputBox.value === ''){
        alert("You must write something");
    }
    else{
        count++;
        let li=document.createElement("li");
        li.innerHTML= inputBox.value;
        listContainer.appendChild(li);
        pendingPara.setAttribute("id","AfterData"); 
        let span=document.createElement("span");
        span.innerHTML = "\u00d7";
        li.appendChild(span);
        dis.innerHTML= `${compcount}/${compcount+count} completed`;
        h1.appendChild(dis);
    }
    savedata();
    inputBox.value="";
};

listContainer.addEventListener("click",function(e){
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        listContainerComp.appendChild(e.target);
        completePara.setAttribute("id","AfterData"); 
        compcount++;
    }
    else if(e.target.tagName === "SPAN"){
        e.target.parentElement.remove();
    }
    savedata();
    count--;
    if(count === 0){pendingPara.setAttribute("id","pending");} 
    dis.innerHTML= `${compcount}/${compcount+count} completed`;
    h1.appendChild(dis);
},false);


listContainerComp.addEventListener("click",function(e){
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        e.target.setAttribute("status","0");
        listContainer.appendChild(e.target);
        pendingPara.setAttribute("id","AfterData"); 
        count++;
    }
    else if(e.target.tagName === "SPAN"){
        e.target.parentElement.remove();
    }
    savedata();
    compcount--;
    if(compcount === 0){completePara.setAttribute("id","complete");} 
    dis.innerHTML= `${compcount}/${compcount+count} completed`;
    h1.appendChild(dis);
},false);

var currentDate = new Date();
var day = currentDate.getDate();
var month = currentDate.getMonth() + 1;
var year = currentDate.getFullYear();

let data={};
let i=0;

function createTask(){
    const inputBox = document.querySelector('.createList');
    const listConatainer = document.querySelector('.create'); // Replace 'your-container-class' with the class of your container
    if (inputBox.value === '') {
        alert("Write the name of the task");
    } else {
        listConatainer.innerHTML += `<div class="box"><br>
            <br><h3>TASK:${inputBox.value} (<span>${day+'-'+month+'-'+year}</span>)</h3>
            <br><button class="view" value=${i} onclick="openWindow(event)">view list</button>
        </div>`;
        data[i]=inputBox.value;
    }
};


function openWindow(event){
    // might have to change for data base
    const dataValue = event.target.value;
    const name=document.getElementById("name");
    name.innerText=`${data[dataValue]}`;
    const todo_app=document.querySelector(".todo-app1");
    todo_app.setAttribute("class","todo-app");
    const home=document.querySelector(".home");
    home.setAttribute("class","home1");
};

function savedata(){
     bigData.pendingTask=listContainer.innerHTML;
     bigData.completeTask=listContainerComp;
}

console.log(bigData);

function update(){
    bigData.count=count;
    bigData.compcount=compcount;
fetch('/process-data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(bigData)
});};
