import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQueryClient } from 'react-query';
import { useMutateAuth } from './useMutateAuth';

export const useProcessAuth = () => {
    const navigation =  useNavigate()
    const queryClient = useQueryClient()
    const [email, setEmail] = useState('')
    const [pw, setPw] = useState('')
    const [isLogin, setIsLogin] = useState(true)
    const {loginMutation, registerMutation, logoutMutation} = useMutateAuth()

    const processAuth = async (e: FormEvent<HTMLFormElement>) => {
        if (isLogin) {
            loginMutation.mutate({
                email: email,
                password: pw,
            })
        } else {
            await registerMutation
            .mutateAsync({
                email: email,
                password: pw,
            })
            .then(() => {
                loginMutation.mutate({
                    email: email,
                    password: pw,
                })
            }) 
            .catch(() => {
                setPw('')
                setEmail('')
            })
        }
    }

    const logout = async () => {
        await logoutMutation.mutateAsync()
        queryClient.removeQueries('tasks')
        queryClient.removeQueries('user')
        queryClient.removeQueries('single')
        navigation('/')
    }
    return { 
        email,
        setEmail,
        pw,
        setPw,
        isLogin,
        setIsLogin,
        processAuth,
        registerMutation,
        loginMutation,
        logout
    }
}
