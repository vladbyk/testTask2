import {useEffect, useState} from "react";
import {BASE_URL, send_request} from "../../components/auth/setAuth";


function CountriesDetail() {
    const [plotImage, setPlotImage] = useState(null)
    useEffect(() => {
        send_request.get(BASE_URL + 'plot/', {
            params: {
                country: window.location.href.match('\\w{1,}$')[0],
                start: '2020-01-01',
                end: '2020-12-31',
            }
        })
            .then((res) => {
                console.log(res)
                setPlotImage('data:image/png;base64, ' + res.data.bytes)
            })
            .catch((err) => {
                console.log(err)
            })
    }, [])
    return (
        <>
            <img className='plot_img' src={plotImage} alt="курс валюты"/>
        </>
    )
}

export default CountriesDetail