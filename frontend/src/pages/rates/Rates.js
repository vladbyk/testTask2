import {useEffect, useState} from "react";
import {BASE_URL, send_request} from "../../components/auth/setAuth";
import "./Rates.css"
import {Link} from "react-router-dom";

function Rates() {
    const [rates, setRates] = useState(null)
    useEffect(()=>{
        send_request(BASE_URL+ 'rates/')
            .then((res)=>{
                setRates(res.data.rates.map((rate)=>{
                    return (<Link className="rates" key={rate.toString()} to={rate}>{rate}</Link>)
                }))
            })
    },[])
    return (
        <>
            <p>Здесь вы можете получить график курса валюты страны к 1 USD</p>
            {rates}
        </>
    )
}

export default Rates