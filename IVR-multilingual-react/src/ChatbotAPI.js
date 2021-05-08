import axios from "axios"

const API = {
  GetChatbotResponse: async (message, lang) => {
    return new Promise(function(resolve, reject) {

      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/abinbev',
        data: {
            "msg": message,
            "lang": lang,
        }
      }).then((res)=> {
        console.log(res);
          if (res.data.length > 1){
            resolve(res.data[0] + "\n" + res.data[1])
            resolve(res.data[1])
          }
          
          if (res.data.length > 2)
            resolve(res.data[0] + "\n" + res.data[1] + "\n" + res.data[2])

          if (res.data.length > 3)
            resolve(res.data[0] + "\n" + res.data[1] + res.data[2] + res.data[3])
          
          resolve(res.data[0])

      }, (e) => {
        console.log(e);
      });

    });
  }
};

export default API;
