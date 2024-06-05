import {
    BrowserRouter,
    Routes,
   Route
} from "react-router-dom";

import Login from "../pages/Login";
import Panel from "../pages/Panel";
import PrivateRoute from "./PrivateRoute";
import { useAuth } from "../hooks/AuthContext";
import Hosts from "../pages/Hosts";
import Profile from "../pages/Profile";
import Host from "../pages/Host";


const Router:React.FC = ()=>{
    const {user} = useAuth()
    
    return (
        <BrowserRouter>
            

            <Routes>
                <Route element={ <Login/>} path="/" ></Route>
                <Route element={ <PrivateRoute component={Panel}/>} path="/panel"  ></Route>
                <Route element={ <PrivateRoute component={Hosts}/>} path="/hosts"  ></Route>
                <Route element={ <PrivateRoute component={Host}/>} path="/host/:ip"  ></Route>
                <Route element={ <PrivateRoute component={Profile}/>} path="/profile/:id"  ></Route>
            </Routes>
        
        </BrowserRouter>
    )

}



export default Router