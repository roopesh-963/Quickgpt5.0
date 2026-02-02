import React, { useEffect, useState, useRef } from 'react'
import { useAppContext } from '../context/AppContext.jsx'
import { assets } from '../assets/assets'
import Message from './Message.jsx'
import toast from 'react-hot-toast'

const Chatbox = () => {
  const containerRef = useRef(null)
  const { selectedChat, theme ,user, axios,token,setUser} = useAppContext()
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const [prompt, setPrompt] = useState('')
  const [mode, setMode] = useState('text')
  const [isPublished, setIsPublished] = useState(false)
  const onSubmit = async (e) => {
    try{
     e.preventDefault()
      if(!user) return toast('Login to send a message')
        setLoading(true)
      const promptCopy = prompt
      setPrompt('')
      setMessages(prev => [...prev, {role:'user', content: prompt, timestamp: Date.now(), isImage: false}])

      const {data} = await axios.post(`/api/message/${mode}`, {chatId: selectedChat._id, prompt, isPublished}, {headers :{Authorization:token}} )
      
      if(data.success){
        setMessages(prev=> [...prev, data.reply])

        if (mode === 'image' ){
        
          setUser(prev => ({...prev, credits:prev.credits -2}) 
          )
        }else{
          setUser (prev => ({...prev, credits: prev.credits -1}) )
        }

      }else{
        toast.error(data.message)
        setPrompt(promptCopy)
      }
    }catch(error){
      toast.error(error.message)
    }finally{
      setPrompt('')
      setLoading(false)
    }

  }
 

 useEffect(() => {
  if (!selectedChat?._id) return
  setMessages(selectedChat.messages || [])
}, [selectedChat?._id])

  
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() =>{
    if(containerRef.current){
      containerRef.current.scrollTo({
        top: containerRef.current.scrollHeight,
        behavior:"smoth",

      })
    }
  },[messages])


  return (
    <div className="
  h-full flex flex-col
  pt-16 md:pt-6
  px-5 md:px-10 xl:px-30
  2xl:pr-40
">


      
      {/* chat messages */}
     <div ref={containerRef} className='flex-1 overflow-y-auto pr-2'>

        {messages.length === 0 && (
          <div className='h-full flex flex-col items-center justify-center gap-2 text-primary'>
            <img
              src={theme === 'dark' ? assets.logo_full_dark : assets.logo_full}
              alt=''
              className='w-full max-w-56 sm:max-w-68'
            />
            <p className='mt-5 text-4xl sm:text-6xl text-center text-gray-400 dark:text-white'>
              Ask me anything.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <Message
            key={message.timestamp + message.role}
            message={message}
          />
        ))}
        {/* Three Dots Loading */}
        {
          loading && <div className='loader flex items-center gap-1.5'>
            <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
            <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
            <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
          </div>
        }

        <div ref={bottomRef} />
      </div>

      {mode === 'image' && (
        <label className='inline-flex items-center gap-2 mb-3 text-sm mx-auto'>
          <p className='text-xs'>Publish Genrated Image to community</p>
          <input type='checkbox' className='cursor-pointer' checked={isPublished}
          onChange={(e)=>setIsPublished(e.target.checked)}/>
        </label>
      )}

      {/* prompt */}
      <form onSubmit={onSubmit} className='bg-primary/20 dark:bg-[#583C79]/30 border border-primary dark:border-[#80609F]/30 rounded-full w-full max-w-2xl p-3 pl-4 mx-auto flex gap-4 items-center'>
        {/* input coming next */}
        <select onChange={(e)=>setMode(e.target.value)} value={mode} className='text-sm pl-3 pr-2 outline-none'>
          <option className='dark:bg-purple-900' value="text">Text</option>
          <option className='dark:bg-purple-900' value="image">Image</option>
        </select>
        <input onChange={(e)=>setPrompt(e.target.value)}  value={prompt} type="text" placeholder='type your prompt here...' className='flex-1 w-full text-sm outline-none' required/>
        <button disabled={loading}>
          <img src={loading ? assets.stop_icon : assets.send_icon } className='w-8 cursor-pointer' alt='' />
        </button>
      </form>
    </div>
  )
}

export default Chatbox
