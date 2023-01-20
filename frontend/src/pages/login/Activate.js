import {useEffect, useState} from "react";
import axios from "axios";
import {BASE_URL} from "../../components/auth/setAuth";


function Activate(){
    const [helpText,setHelpText] = useState('')
    useEffect(()=>{
        const activate_href = window.location.href.match('[=](.{1,})')
        axios.get(BASE_URL + 'account/', {
            params: {
                token: activate_href[1]
            },
        })
        .then((res)  =>{
            axios.post(BASE_URL + 'jwt/refresh/',{
                refresh: activate_href[1]
            })
            .then((res)=>{
                sessionStorage.setItem('access',res.data.access)
                sessionStorage.setItem('refresh',res.data.refresh)
                window.location.assign('/')
            })
        })
        .catch((err)=>{
            setHelpText(<span>Не удалось активировать аккаунт!</span>)
        })
    },[])


    return(
        <>
            {helpText}
        </>
    )
}

export default Activate