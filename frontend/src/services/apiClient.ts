import axios from "axios"
import { io } from "socket.io-client"


const api = axios.create({
    //https://my--menu.herokuapp.com/
    baseURL:"http://127.0.0.1:5001/" ,
})

const socketAddress = "http://localhost:5002/main"

const socket = io(socketAddress)

export{
    api, socket
}