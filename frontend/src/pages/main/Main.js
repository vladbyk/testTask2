import {BASE_URL, send_request} from "../../components/auth/setAuth";
import {useEffect, useState} from "react";
import Select from "react-select"
import "./Main.css"

function getDaysArray(start, end) {
    let arr = []
    for (let dt = new Date(start); dt <= new Date(end); dt.setDate(dt.getDate() + 1)) {
        arr.push(new Date(dt))
    }
    return arr
}

function correctDate(val) {
    if (val < 10) {
        return `0${val}`
    } else return val
}

function getArrDates() {
    return getDaysArray('2020-01-01', '2020-12-31').map((day) => {
        return (
            {
                value: `${day.getFullYear()}-${day.getMonth() + 1}-${day.getDate()}`,
                label: `${day.getFullYear()}-${correctDate(day.getMonth() + 1)}-${correctDate(day.getDate())}`,
            }
        )
    })
}


function Main() {
    const [countries, setCountries] = useState(null)
    const [currentCountry, setCurrentCountry] = useState(null)
    const [startDate, setStartDate] = useState(null)
    const [endDate, setEndDate] = useState(null)
    const [endDates, setEndDates] = useState(null)
    const [startDates, setStartDates] = useState(null)
    const [submitFlag, setSubmitFlag] = useState(false)
    const [endStyles, setEndStyles] = useState('notActive')
    const [plotImage, setPlotImage] = useState(null)
    useEffect(() => {
        getCountres()
        setStartDates(getArrDates())
    }, [])

    function getCountres() {
        send_request.get(BASE_URL + "countres/")
            .then((res) => {
                setCountries(res.data.map((countries) => {
                    return (
                        {
                            value: countries.country,
                            label: countries.country.charAt(0).toUpperCase() + countries.country.slice(1)
                        }
                    )
                }))
            })
    }

    const changeCountryHundler = (country) => {
        setCurrentCountry(country.value)
    }

    const changeStartDateHundler = (date) => {
        setStartDate((date.value))
    }

    const changeEndDateHundler = (date) => {
        setEndDate((date.value))
    }
    useEffect(() => {
        if (startDate != null) {
            setEndDates(
                getDaysArray(startDate, '2020-12-31').map((day) => {
                    return (
                        {
                            value: `${day.getFullYear()}-${day.getMonth() + 1}-${day.getDate()}`,
                            label: `${day.getFullYear()}-${correctDate(day.getMonth() + 1)}-${correctDate(day.getDate())}`,
                        }
                    )
                })
            )
            setEndStyles('')
        }
    }, [startDate])

    useEffect(() => {
        if (startDate != null && endDate != null && currentCountry != null) {
            setSubmitFlag(true)
        }
    }, [startDate, endDate, currentCountry])

    const submitHundler = () => {
        send_request.get(BASE_URL + 'plot/', {
            params: {
                country: currentCountry,
                start: startDate,
                end: endDate,
            }
        })
            .then((res) => {
                console.log(res)
                setPlotImage('data:image/png;base64, ' + res.data.bytes)
            })
            .catch((err) => {
                console.log(err)
            })
    }

    return (
        <div className="main_block">
            <p>Здесь вы можете получить график распространения коронавируса за определенный промежуток времени 2020 года</p>
            <p>Выберите страну</p>
            <Select onChange={changeCountryHundler} options={countries}/>
            <p>Выберите промежуток времени</p>
            <div className="range_date">
                <Select onChange={changeStartDateHundler} options={startDates}/>
                <Select onChange={changeEndDateHundler} options={endDates} className={endStyles}/>
            </div>
            {submitFlag && <input type='submit' onClick={submitHundler} className="country_info_button"/>}
            <img className='plot_img' src={plotImage} alt={currentCountry}/>
        </div>
    );
}

export default Main;