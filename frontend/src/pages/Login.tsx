import {
    Box,
    Flex,
    Stack,
    Heading,
    Text,
    Container,
    Input,
    Button,
    SimpleGrid,
    Avatar,
    AvatarGroup,
    useBreakpointValue,
    IconProps,
    Icon,
    useColorModeValue,
    Image,
    Center
  } from '@chakra-ui/react';
import { ColorModeSwitcher } from '../components/ColorModeSwitcher';
import { useToast } from '@chakra-ui/react'
import { useState } from 'react';
import { useAuth } from '../hooks/AuthContext';
import Loader from '../components/Loader';

  
  export default function JoinsUs() {

    const [username,setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const {signIn} = useAuth()
   
    const toast = useToast()

    const onHandleSubmit = async (e:any)=>{
      setIsLoading(true)
      
      e.preventDefault()

      if(username === "" || password === ""){
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

      
      signIn({username,password})
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

    return (
      
      <Box   w="100%">
       
        <Loader isLoading={isLoading} />
        <Flex pt="6" w="100%" justifyContent={"center"} alignItems={"center"}>
          <Center>
           
          <Stack 
            bg={"gray.700"}
            rounded={'xl'}
            p={{ base: 4, sm: 6, md: 8 }}
            spacing={{ base: 8 }}
            color={"gray.100"}
            w="100%">
            <Stack  w="100%" spacing={4}>
              <Heading
                color={"gray.100"}
                lineHeight={1.1}
                fontSize={{ base: '2xl', sm: '3xl', md: '4xl' }}>
                Log-In
                
              </Heading>
              <Text color={"gray.500"} fontSize={{ base: 'sm', sm: 'md' }}>
                For employees only
              </Text>
            </Stack>
            <Box onSubmit={onHandleSubmit} as={'form'} mt={10}>
              <Stack spacing={4}>
              <Text  color={"gray.200"} fontSize={{ base: 'sm', sm: 'md' }}>
                Username:
              </Text>
                <Input
                  placeholder="username"
                  bg={'gray.500'}
                  border={0}
               
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
     
          </Stack>

          </Center>
        </Flex>

        <Blur
          position={'absolute'}
          top={-39}
          left={-200}
        
          style={{ filter: 'blur(70px)' }}
        />
      </Box>
    );
  }
  
  export const Blur = (props: IconProps) => {

    const breakPointW = useBreakpointValue({ base: '100%', md: '40vw', lg: '30vw' })
    const breakPointZIndex = useBreakpointValue({ base: -1, md: -1, lg: 0 })
    return (
      <Icon
        width={breakPointW}
        zIndex={breakPointZIndex}
        height="560px"
        viewBox="0 0 528 560"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"

        {...props}>
        <circle cx="71" cy="61" r="111" fill="#F56565" />
        <circle cx="244" cy="106" r="139" fill="#ED64A6" />
        <circle cy="291" r="139" fill="#ED64A6" />
        <circle cx="80.5" cy="189.5" r="101.5" fill="#ED8936" />
        <circle cx="196.5" cy="317.5" r="101.5" fill="#ECC94B" />
        <circle cx="70.5" cy="458.5" r="101.5" fill="#48BB78" />
        <circle cx="426.5" cy="-0.5" r="101.5" fill="#4299E1" />
      </Icon>
    );
  };