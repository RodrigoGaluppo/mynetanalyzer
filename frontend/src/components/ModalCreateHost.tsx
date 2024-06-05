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
    Select,
    useToast,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalCloseButton,
    ModalBody,
    ModalFooter
  } from '@chakra-ui/react';


import { useEffect, useState } from 'react';
import {api} from '../services/apiClient';
import Loader from './Loader';
import { useAuth } from '../hooks/AuthContext';

interface IHost{
  id:number;
  name:string;
  created_at:string;
  ip:string;
}

  

  export default function ModalEditHost({isOpen,onClose}: {isOpen:boolean, onClose:()=>void}) {

    const [Name, setName] = useState("")
    const [IP, setIP] = useState("")
  

    const [isLoading,setIsLoading] = useState(false)
    const {token} = useAuth()

    const toast = useToast()



    function onHandleSubmit(){


      if(Name == "" || IP == "" )
      {
        toast({
          title: 'Invalid fields',
          description: "one or more fields can not be empty",
          status: 'error',
          duration: 9000,
          isClosable: true,
          position:"top-left"
        })
            
        return
      }
    
     
      setIsLoading(true)
      api.post("hosts",{
        name:Name,
        ip:IP
        
       },{ headers: {"Authorization" : `Bearer ${token}`}})
      .then(()=>{
        toast({
          title: Name + " host created successfully" ,
          description: "",
          status: 'success',
          duration: 9000,
          isClosable: true,
          position:"top-left"
        })
        onClose()
        setIsLoading(false)
      })
      .catch((err)=> {

        console.log(err)
        toast({
          title: 'Erro',
          description: "could not create host",
          status: 'error',
          duration: 9000,
          isClosable: true,
          position:"top-left"
        })
        setIsLoading(false)
        return
      })

    }

    return (
        <Modal  
        isOpen={isOpen}
        onClose={onClose}
      >
        <Loader isLoading={isLoading} />
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create a Host</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <Container
            maxW={'7xl'}
            w="100%"
            py={2}>
    
            <Stack
                bg={useColorModeValue('gray.100', 'gray.700')}
                rounded={'xl'}
                p={{ base: 4 }}
                spacing={{ base: 8 }}
                maxW={{ lg: 'lg' }}>
                <Stack spacing={4}>
                <Heading
                    color={useColorModeValue('gray.800', 'gray.50')}
                    lineHeight={1.1}
                    fontSize={{ base: '2xl', sm: '3xl', md: '4xl' }}>
                    Create a Host
                    <Text
                    as={'span'}
                    bgGradient="linear(to-r, red.400,pink.400)"
                    bgClip="text">
                    !
                    </Text>
                </Heading>
                
                </Stack>
                <Box as={'form'} mt={10}>
                <Stack spacing={4}>
        
                <Text color={useColorModeValue('gray.500', 'gray.200')} fontSize={{ base: 'sm', sm: 'md' }}>
                    Name:
                    </Text>
                    <Input
                    placeholder="Name"
                    bg={'gray.100'}
                    border={0}
                    color={'gray.500'}
                    _placeholder={{
                        color: 'gray.500',
                    }}
                    
                    onChange={(e)=>{
                        setName(e.target.value)
                    }}
                    />
                    <Text color={useColorModeValue('gray.500', 'gray.200')} fontSize={{ base: 'sm', sm: 'md' }}>
                    IP:
                    </Text>
                    <Input
                    placeholder="IP"
                    bg={'gray.100'}
                    border={0}
                    color={'gray.500'}
                    _placeholder={{
                        color: 'gray.500',
                    }}
                    onChange={(e)=>{
                        setIP(e.target.value)
                    }}
                    />

                
                
                </Stack>
                <Button
                    fontFamily={'heading'}
                    mt={8}
                    w={'full'}
                    bgGradient="linear(to-r, red.400,pink.400)"
                    color={'white'}
                    _hover={{
                    bgGradient: 'linear(to-r, red.400,pink.400)',
                    boxShadow: 'xl',
                    }}
                    onClick={onHandleSubmit}
                    >
                    Submit
                </Button>
                </Box>
                form
            </Stack>
            </Container>
        </ModalBody>
  
    <ModalFooter>
        <Button onClick={()=>{onHandleSubmit()}} colorScheme='pink' mr={3}>
        Send
        </Button>
        <Button onClick={onClose}>Cancel</Button>
    </ModalFooter>
    </ModalContent>
    </Modal>
    );
  }
  
  