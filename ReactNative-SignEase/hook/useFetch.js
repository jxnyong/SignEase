import axios from "axios";
import { useEffect, useState } from "react";
import { config } from "../components"

const useFetch = (endpoint, query) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const fetchData = () => {
        setLoading(true);
        try {
            axios.post(`${config.backendUrl}${endpoint}`, query )
            .then((response) => {
                setData(response.data);
            });
        } catch (error){
            setError(error);
        } finally {
            setLoading(false);
        }
    }
    useEffect(() => {
        fetchData();
    },[]);
    const refetch = () => {
        setLoading(true);
        fetchData();
    }
    return {data, loading, error, refetch}
}
export default useFetch;