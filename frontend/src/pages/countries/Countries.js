import {useEffect, useState} from "react";
import {BASE_URL, send_request} from "../../components/auth/setAuth";
import "./Countries.css"
import {Link} from "react-router-dom";

function Countries() {
    const [countries, setCountries] = useState(null)
    useEffect(() => {
        send_request.get(BASE_URL + 'countres/')
            .then((res) => {
                console.log(res.data)
                setCountries(res.data.map((countries)=>{
                    return <Link className="countries" key={countries.id} to={countries.country}> {countries.country.charAt(0).toUpperCase() + countries.country.slice(1)} </Link>
                }))
            })
        console.log(countries)
    }, [])

    return (
        <>
            <p>Здесь вы можете получить график распространения коронавируса страны за 2020 год</p>
            {countries}
        </>
    )
}

export default Countries