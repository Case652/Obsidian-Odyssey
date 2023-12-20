import React from 'react';
import { useOutletContext} from "react-router-dom";
import {useFormik} from 'formik'
import * as yup from 'yup'

function Signup() {
    const {setSignup,signup,setUser,navigate} = useOutletContext();
    const signupSchema = yup.object().shape({
        username: yup.string().min(1,'Must Be?').max(50,'Less is better.').required('Username is required'),
        password: yup.string().min(1,'Must Be?').max(72,'Less is better.').required('Password is required'),
        confirmPassword: signup ? yup.string().oneOf([yup.ref('password'), null], 'Passwords must match').required('Confirm Password is required'): undefined,
    })
    const formik = useFormik({
        initialValues:{
            username:'',
            password:'',
            confirmPassword:'',
        },
        validationSchema: signupSchema,
        onSubmit: (values) => {
            if (signup && values.password !== values.confirmPassword) {
                console.log('Passwords do not match');
                return;
            }
            const endpoint = signup ? '/users' : '/login'
            fetch(endpoint,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(values)
            }).then((r)=>{
                if (r.ok) {
                    r.json().then(({user})=> {
                        setUser(user);
                        navigate('/')
                    })
                } else {
                    console.log('errors')
                }
            })
        }
    })

    function toggleSignup () {
        setTimeout(()=>{
            setSignup((currentSignup) => !currentSignup);
        },500);
        
        const signupIn = document.querySelector('.form-outline');
        signupIn.classList.add('flip');
        setTimeout(()=>{
            signupIn.classList.remove('flip');
        },800)
    }
    return (
        <section className='signup-in'>
            <div className='form-outline'>
                
                <div className="signup-form" >
                <h2 className='h2-title'>{signup ? 'Register': 'Login'}</h2>
                <form onSubmit={formik.handleSubmit}>
                    <div className='box-input'>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formik.values.username}
                            onChange={formik.handleChange}
                            required
                            placeholder=' '
                        />
                        <label htmlFor="username" >Username</label>
                        {formik.touched.username && formik.errors.username ? (<div className="error">{formik.errors.username}</div>) : null}
                    </div>
                    <div className='box-input'>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formik.values.password}
                            onChange={formik.handleChange}
                            required
                            placeholder=' '
                        />
                        <label htmlFor="password">Password</label>{formik.touched.password && formik.errors.password ? (<div className="error">{formik.errors.password}</div>) : null}
                    </div>
                    {signup && 
                    <div className='box-input'>
                        <input
                            type="password"
                            id="confirmPassword"
                            name="confirmPassword"
                            value={formik.values.confirmPassword}
                            onChange={formik.handleChange}
                            required
                            placeholder=' '
                        />
                        <label htmlFor="confirmPassword">Confirm Password</label>
                        {formik.touched.confirmPassword && formik.errors.confirmPassword ? (<div className="error">{formik.errors.confirmPassword}</div>) : null}
                    </div>}
                    <button className='login-button' type="submit">{signup ? 'Sign Up': 'Login'}</button>
                </form>
                <button className='signin-out-button' onClick={toggleSignup}>{signup ? 'Already have an account? Login': 'Dont have an account? Sign Up'}</button>
            </div>
        </div>
    </section>
    )
}
export default Signup;