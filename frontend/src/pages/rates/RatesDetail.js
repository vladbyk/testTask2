import {useEffect, useState} from "react";
import {BASE_URL, send_request} from "../../components/auth/setAuth";


function RatesDetail() {
    const [plotImage, setPlotImage] = useState(null)
    useEffect(() => {
        send_request(BASE_URL + `change-rates/${window.location.href.match('\\w{1,3}$')[0]}`)
            .then((res) => {
                setPlotImage('data:image/png;base64, ' + res.data.bytes)
            })
    }, [])
    return (
        <>
            <img className='plot_img' src={plotImage} alt="курс валюты"/>
        </>
    )
}

export default RatesDetail