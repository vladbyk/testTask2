import {useEffect, useRef, useState} from "react"
import "./Login.css"
import axios from "axios"
import {BASE_URL} from "../../components/auth/setAuth"

function Login() {
    const emailInputRef = useRef(null)
    const emailRegInputRef = useRef(null)
    const passwordInputRef = useRef(null)
    const passwordRegInputRef = useRef(null)
    const passwordRegReplayInputRef = useRef(null)
    const [helpText, setHelpText] = useState('')
    const [styleForm, setStyleForm] = useState({
        login: "flex",
        registration: "none",
    })
    const submitRegistrationHandler = () => {
        let reg = /^.*(?=.{8,})(?=.*[A-Z])(?=.*\d).*$/
        if (!reg.test(passwordRegInputRef.current.value)) {
            setHelpText(
                <span>Пароль должен быть не менее 8 символов, содержить как минимум 1 заглавную букву и цифру.</span>)
        }
        else if (passwordRegInputRef.current.value === passwordRegReplayInputRef.current.value) {
            axios.post(BASE_URL + 'account/', {
                email: emailRegInputRef.current.value,
                password: passwordRegInputRef.current.value
            })
            .catch((err) => {
                console.log(err)
                setHelpText(<span>Учетная запись с такой почтой уже существует.</span>)
            })
        }
        else{
            setHelpText(<span>Ваши пароли не совпадают.</span>)
        }
    }
    const submitLoginHandler = () =>{
        axios.post(BASE_URL + 'jwt/create/', {
            email: emailInputRef.current.value,
            password: passwordInputRef.current.value
        })
        .then((res) => {
            sessionStorage.setItem('access', res.data.access)
            sessionStorage.setItem('refresh', res.data.refresh)
            window.location.assign('/')
        })
        .catch((err) => {
            console.log(err)
            setHelpText(<span>Такого аккаунта не существует.</span>)
        })
    }
    const formClick = () => {
        if (styleForm.login === "none"){
            setStyleForm({
                login:'flex',
                registration: "none"
            })
        } else {
            setStyleForm({
                login: 'none',
                registration: "flex"
            })
        }
        setHelpText('')
    }
    return (
        <div>
            <div className="login_form" style={{display: styleForm.login}}>
                <p onClick={formClick}>Вход</p>
                {helpText}
                <input name="email" type="email" ref={emailInputRef} autoComplete="off" placeholder="Почта"/>
                <input name='password' type="password" ref={passwordInputRef} autoComplete="off" placeholder="Пароль"/>
                <input type="submit" value="Вход" onClick={submitLoginHandler}/>
            </div>
            <div className="registration_form" style={{display: styleForm.registration}}>
                <p onClick={formClick}>Регистрация</p>
                {helpText}
                <input name="email" type="email" ref={emailRegInputRef} autoComplete="off" placeholder="Почта"/>
                <input name='password' type="password" ref={passwordRegInputRef} autoComplete="off" placeholder="Пароль"/>
                <input name="passwordReplay" type="password" ref={passwordRegReplayInputRef} autoComplete="off" placeholder="Повторите пароль"/>
                <input type="submit" value="Регистрация" onClick={submitRegistrationHandler}/>
            </div>
        </div>
    )
}

export default Login;