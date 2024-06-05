import { Center, Flex, Grid, GridItem, Heading, Icon, SimpleGrid, useColorModeValue,Text, Box, VStack, Button, ButtonGroup } from "@chakra-ui/react";

import PanelGrid from "../components/PanelGrid";
import SidebarWithHeader from "../components/SideBar";

import { useAuth } from "../hooks/AuthContext";
import { api } from "../services/apiClient";
import { useEffect, useState } from "react";
import ModalCreateHost from "../components/ModalCreateHost";
import { FaEye, FaPen, FaTrash } from "react-icons/fa";
import Loader from "../components/Loader";
import { useNavigate } from "react-router-dom";

interface Machine{
  id:number;
  name:string;
  created_at:string;
  ip:string;
}

interface charData{
  data:number[],
  labels:string[]
}

export default function Hosts() {
 
  
  const {token,user} = useAuth()

  const navigate = useNavigate()
  
  const [isOpen,setIsOpen] = useState(false)

  const [machines,setMachines] = useState({} as Machine[])

  const [isLoading,setIsLoading] = useState(false)

 useEffect(()=>{
  setIsLoading(true)
  api.get("hosts", { headers: {"Authorization" : `Bearer ${token}`}})
  
  .then((res)=>{
    setMachines(res.data)
    setIsLoading(false)
  })
  .catch((err)=>{
    console.log(err)
    setIsLoading(false)
  })
 },[])


  function deleteHost(id:number){

    if((window.confirm("are you sure you want to delete host with id " + id.toString())) == false ){
      return
    }

    setIsLoading(true)

    api.delete(`hosts/${id}`, { headers: {"Authorization" : `Bearer ${token}`}})
    .then((res)=>{

      setIsLoading(false)
    })
    .catch(()=>{
      setIsLoading(false)
    })

  }


  return (
    <>
    <Loader isLoading={isLoading} />
    <SidebarWithHeader>
      <PanelGrid/>
      <SimpleGrid color="white" my="10" columns={1} spacing="6" >

    
      <Flex flexWrap={"wrap"}>
      <Heading w="100%" textAlign={"center"}></Heading>
        <Button
        onClick={()=>{
          setIsOpen(true)
        }}
        colorScheme="pink">
          Add Host
        </Button>
        <SimpleGrid mt="4" columns={[1,1,3]} spacing={"4"} w="100%">
          
          {
            !!!!machines && machines?.length > 0 ? machines?.map((h)=>(
              <Center justifyContent={"space-between"} p="4" _hover={{opacity:0.9}} bg={"gray.700"} color={"white"}>
                <Text>{h.name} - {h.ip}</Text>
                <ButtonGroup>
                    <Button onClick={()=>{
                      navigate("/host/" + h.ip)
                      
                    }} colorScheme="green">
                      <FaEye></FaEye>
                    </Button>

                    <Button colorScheme="yellow">
                      <FaPen></FaPen>
                    </Button>

                    <Button onClick={()=>{
                      deleteHost(h.id)
                    }} colorScheme="red">
                      <FaTrash></FaTrash>
                    </Button>
                </ButtonGroup>
                
              </Center>
            ))

            :

            <></>
          }

         
        </SimpleGrid>
  
        
      </Flex>

      </SimpleGrid>

      <ModalCreateHost
       isOpen={isOpen}
        onClose={()=>{
          setIsOpen(false)
        }}

       />

     
    </SidebarWithHeader>
    </>
  );
}