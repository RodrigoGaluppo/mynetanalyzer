import { Center, Flex, Grid, GridItem, Heading, Icon, SimpleGrid, useColorModeValue,Text, Box, VStack } from "@chakra-ui/react";
import { FaBook, FaPlay, FaUser } from "react-icons/fa";
import PieChart from "../components/PieChart";
import LineChart from "../components/LineChart";
import PanelGrid from "../components/PanelGrid";
import SidebarWithHeader from "../components/SideBar";
import { useEffect, useState } from "react";
import {socket} from "../services/apiClient";
import { useAuth } from "../hooks/AuthContext";
import BarChart from "../components/BarChart";
import DoughnutChart from "../components/PieChart";

interface charData{
  data:number[],
  labels:string[]
}

export default function Panel() {
 
  

  const {token,user} = useAuth()
  
  const [chart30Data, setChart30Data] = useState({} as charData)
  const [chart60Data, setChart60Data] = useState({} as charData)
  const [chart12HData, setChart12HData] = useState({} as charData)
  const [chart24HData, setChart24HData] = useState({} as charData)

  const [chartprotocolsData, setChartprotocolsData] = useState({} as charData)
  const [chartsourcePortsData, setChartsourcePortsData] = useState({} as charData)
  const [chartDestPortsData, setChartDestPortsData] = useState({} as charData)

  const [chartHostBySizePackets, setChartHostBySizePackets] = useState({} as charData)
  const [chartHostByNumberPackets, setChartHostByNumberPackets] = useState({} as charData)


   // Function to fetch data
   function fetchData() {
    socket.emit("hello")
    socket.emit('request_data_30')
   
    socket.emit('request_data_60')
    socket.emit('request_data_12h')
    socket.emit('request_data_24h')
    socket.emit('request_data_protocols')

    socket.emit('request_data_sourceports')
    socket.emit('request_data_destports')

    socket.emit('request_host_by_number_packets')
    socket.emit('request_host_by_size_packets')
    }


   
    useEffect(() => {
      fetchData()
   
      //Implementing the setInterval method
      const interval = setInterval(fetchData, 5000);

      //Clearing the interval
      return () => clearInterval(interval);
    }, []);


    socket.on('data_update_30', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))

        setChart30Data({
          data:quantities,
          labels:timestamps
        })

      
    });

    socket.on('data_update_60', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))
      
        setChart60Data({
          data:quantities,
          labels:timestamps
        })
    });

    
    socket.on('data_update_12h', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))
      

        setChart12HData({
          data:quantities,
          labels:timestamps
        })
    });

    socket.on('data_update_24h', function(data) {
        

        data = JSON.parse(data)

        // Extract timestamp and quantity
        var timestamps = data.map((d:any)=> (d.timestamp))
        var quantities = data.map((d:any)=> (d.quantity))
      
        setChart24HData({
          data:quantities,
          labels:timestamps
        })
    });



    socket.on('data_update_protocols', function(data) {
        

        data = JSON.parse(data)

        var protocols = data.map((d:any)=> (d.protocol))
        var quantities = data.map((d:any)=> (d.count))

        setChartprotocolsData({
          data:quantities,
          labels:protocols
        })
    });


    socket.on('data_update_sourceports', function(data) {
        

        data = JSON.parse(data)

        var ports = data.map((d:any)=> (d.port))
        var quantities = data.map((d:any)=> (d.count))

        
        setChartsourcePortsData({
          data:quantities,
          labels:ports
        })
    });


    socket.on('data_update_destports', function(data) {
        

        data = JSON.parse(data)

        var ports = data.map((d:any)=> (d.port))
        var quantities = data.map((d:any)=> (d.count))

        setChartDestPortsData({
          data:quantities,
          labels:ports
        })
    });

    socket.on('host_by_number_packets', function(data) {
        
        data = JSON.parse(data)

        var ips = data.map((d:any)=> (d.ip_address))
        var quantities = data.map((d:any)=> (d.count))

        setChartHostByNumberPackets({
          data:quantities,
          labels:ips
        })
    });

    socket.on('host_by_size_packets', function(data) {
        
        data = JSON.parse(data)

        var ips = data.map((d:any)=> (d.ip_address))
        var quantities = data.map((d:any)=> (d.count))

        setChartHostBySizePackets({
          data:quantities,
          labels:ips
        })
    });




  return (
    <>
    <SidebarWithHeader>
      <PanelGrid/>
      <SimpleGrid color="white" my="10" columns={1} spacing="6" >

    
      <Flex flexWrap={"wrap"}>
      <Heading w="100%" textAlign={"center"}></Heading>

      

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 30 minutes</Text>
          <LineChart
            labels={chart30Data.labels}
            data={chart30Data.data}
          />
      </Center>

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 60 minutes</Text>
          <LineChart
            labels={chart60Data.labels}
            data={chart60Data.data}
          />
      </Center>

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 12 hours</Text>
          <LineChart
            labels={chart12HData.labels}
            data={chart12HData.data}
          />
      </Center>

      <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} my="20"  flexWrap={"wrap"} >
        <Text mb="2" textAlign={"center"} w="100%">Packet flow in MB 24 hours</Text>
          <LineChart
            labels={chart24HData.labels}
            data={chart24HData.data}
          />
      </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Protocols</Text>
          <PieChart
            label={chartprotocolsData.labels}
            data={chartprotocolsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Protocols</Text>
          <BarChart
              labels={chartprotocolsData.labels}
              data={chartprotocolsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Source Ports</Text>
          <DoughnutChart
            label={chartsourcePortsData.labels}
            data={chartsourcePortsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Destination Ports</Text>
          <DoughnutChart
            label={chartDestPortsData.labels}
            data={chartDestPortsData.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Top hosts by number of packets</Text>
          <BarChart
            labels={chartHostByNumberPackets.labels}
            data={chartHostByNumberPackets.data}
          />
        </Center>

        <Center  w={{"sm":"100%","md":"50%","lg":"50%"}} flexWrap={"wrap"} maxH="400px" my="20" >
          <Text mb="2" textAlign={"center"} w="100%">Top hosts by size of packets</Text>
          <BarChart
            labels={chartHostBySizePackets.labels}
            data={chartHostBySizePackets.data}
          />
        </Center>
       
  
        
      </Flex>

      </SimpleGrid>
    </SidebarWithHeader>
    </>
  );
}