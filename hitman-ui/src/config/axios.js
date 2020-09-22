import Axios from 'axios';
import { configure } from 'axios-hooks';

const axios = Axios.create({
  baseURL: `${process.env.REACT_APP_API_URL}`,
});

configure({ axios });

export default axios;
