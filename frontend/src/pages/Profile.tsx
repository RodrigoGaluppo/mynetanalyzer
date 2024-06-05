import { Center, Flex, Grid, GridItem, Heading, Icon, SimpleGrid, useColorModeValue,Text, Box, VStack, Button, ButtonGroup, useToast, Input, Stack } from "@chakra-ui/react";

import PanelGrid from "../components/PanelGrid";
import SidebarWithHeader from "../components/SideBar";

import { useAuth } from "../hooks/AuthContext";
import { api } from "../services/apiClient";
import { useEffect, useState } from "react";
import { FaEye, FaPen, FaTrash } from "react-icons/fa";
import Loader from "../components/Loader";
import { useNavigate, useParams } from "react-router-dom";


export default function Profile() {
 
  
  const {token,user} = useAuth()

  const [username,setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const {id} = useParams()
  const {signIn} = useAuth()
 
  const toast = useToast()

  const onHandleSubmit = async (e:any)=>{
    setIsLoading(true)
    
    e.preventDefault()

    if(password === ""){
      toast({
        title: 'Invalid fields',
        description: "username or password can not be empty",
        status: 'error',
        duration: 9000,
        isClosable: true,
        position:"top-left"
      })

      return
    }

    
    api.put("users/"+ user?.id,{password},
    { headers: {"Authorization" : `Bearer ${token}`}}
    )
    .then(res=>{
      toast({
        title: 'success',
        description: "",
        status: 'success',
        duration: 9000,
        isClosable: true, position:"top-left"
      })
      window.location.replace('/panel');
      setIsLoading(false)
    })
    .catch((err)=>{
      console.log(err);
      
      try{
        toast({
          title: 'Invalid fields',
          description: err.response.data.message,
          status: 'error',
          duration: 9000,
          isClosable: true,
          position:"top-left"
        })
      }catch{
        toast({
          title: 'network error',
          description: "could not contact the server",
          status: 'error',
          duration: 9000,
          isClosable: true,
          position:"top-left"
        })
      }

      setIsLoading(false)
    })


  }
  


 useEffect(()=>{
  setIsLoading(true)
  api.get("users/"+ id)
  
  .then((res)=>{
    
    setUsername(res.data?.username)
    setIsLoading(false)
  })
  .catch((err)=>{
    console.log(err)
    setIsLoading(false)
  })
 },[])


  


  return (
    <>
    <Loader isLoading={isLoading} />
    <SidebarWithHeader>
     <Center>
        <VStack>
        <Box onSubmit={onHandleSubmit} as={'form'} mt={10}>
              <Stack spacing={4}>
              <Text  color={"gray.200"}  fontSize={{ base: 'sm', sm: 'md' }}>
                Username:
              </Text>
                <Input
                  placeholder="username"
                  bg={'gray.500'}
                  border={0}
                  defaultValue={username}
                  disabled
                  color={'gray.900'}
                  background={"gray.500"} 
                  _placeholder={{
                    color: 'gray.500',
                  }}
                  onChange={e =>{ setUsername(e.target.value.toString()) }}
                />
                <Text color={useColorModeValue('gray.500', 'gray.200')} fontSize={{ base: 'sm', sm: 'md' }}>
                Password:
                </Text>
                <Input

                  onChange={e =>{ setPassword(e.target.value.toString()) }}
                  placeholder="password"
                  background={"gray.500"} 
                  border={0}
                  type='password'
                  color={'gray.900'}
                  _placeholder={{
                    color: 'gray.500',
                  }}


                />
               
              </Stack>
              
              <Input
                fontFamily={'heading'}
                mt={8}
                type='submit'
                w={'full'}
                bgGradient="linear(to-r, red.400,pink.400)"
                color={'white'}
                _hover={{
                  bgGradient: 'linear(to-r, red.400,pink.400)',
                  boxShadow: 'xl',
                }} />
              
            </Box>
        </VStack>
     </Center>
    </SidebarWithHeader>
    </>
  );
}