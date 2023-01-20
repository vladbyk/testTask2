import ReactDOM from 'react-dom/client';
import {BrowserRouter, Routes, Route} from "react-router-dom";
import './index.css';
import App from './App';
import Login from "./pages/login/Login";
import Activate from "./pages/login/Activate";
import Countries from "./pages/countries/Countries";
import Main from "./pages/main/Main";
import Rates from "./pages/rates/Rates";
import RatesDetail from "./pages/rates/RatesDetail";
import CountriesDetail from "./pages/countries/CountriesDetail";
import Redirect from "./components/Redirect/Redirect";

export default function Routing() {
    let isLoggedIn = !!sessionStorage.getItem('access');
    return (
        <BrowserRouter>
            {isLoggedIn && <App/>}
            <Routes>
                <Route path='/login' element={<Login/>}/>
                <Route path='/activate' element={<Activate/>}/>
                {isLoggedIn && <Route path='/' element={<Main/>}/>}
                {isLoggedIn && <Route path='/countries' element={<Countries/>}/>}
                {isLoggedIn && <Route path='/countries/:name' element={<CountriesDetail/>}/>}
                {isLoggedIn && <Route path='/rates' element={<Rates/>}/>}
                {isLoggedIn && <Route path='/rates/:name' element={<RatesDetail/>}/>}
                <Route path='*' element={<Redirect/>}/>
            </Routes>
        </BrowserRouter>
    )
}

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <Routing/>
);

