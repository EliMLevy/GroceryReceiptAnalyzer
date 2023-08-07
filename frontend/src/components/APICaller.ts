export const getData = async function () {
  const requestOptions: RequestInit = {
    method: 'GET',
    redirect: 'follow',
  };
  console.log(process.env.API + '/data');
  try {
    const response = await fetch(process.env.API + '/data', requestOptions);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error);
  }
};

export const storeNewList = async function (data: any, date: any) {
  const raw = JSON.stringify(data);

  const requestOptions: RequestInit = {
    method: 'POST',
    body: raw,
    redirect: 'follow',
  };

  try {
    const response = await fetch(
      process.env.API + '/storelist?' + 'date=' + date,
      requestOptions
    );
    const result = await response.text();
    console.log(result);
    return true
  } catch (error) {
    console.log(error);
  }
};

export const addTag = async function (id: string, tag: string){
  const raw = JSON.stringify({
    id, tag
  });

  const requestOptions: RequestInit = {
    method: 'POST',
    body: raw,
    redirect: 'follow',
  };

  try {
    const response = await fetch(
      process.env.API + '/addtag',
      requestOptions
    );
    const result = await response.text();
    console.log(result);
    return true
  } catch (error) {
    console.log(error);
  }
}

export const removeTag = async function (id: string, tag: string){
  const raw = JSON.stringify({
    id, tag
  });

  const requestOptions: RequestInit = {
    method: 'POST',
    body: raw,
    redirect: 'follow',
  };

  try {
    const response = await fetch(
      process.env.API + '/removetag',
      requestOptions
    );
    const result = await response.text();
    console.log(result);
    return true
  } catch (error) {
    console.log(error);
  }
}


export const getExpensesByTag = async function () {
  const requestOptions: RequestInit = {
    method: 'GET',
    redirect: 'follow',
  };
  try {
    const response = await fetch(process.env.API + '/analysis/bytag', requestOptions);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error);
  }
};

export const getExpensesByWeek = async function () {
  const requestOptions: RequestInit = {
    method: 'GET',
    redirect: 'follow',
  };
  try {
    const response = await fetch(process.env.API + '/analysis/byweek', requestOptions);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error);
  }
};


export const getTopTenExpenses = async function () {
  const requestOptions: RequestInit = {
    method: 'GET',
    redirect: 'follow',
  };
  try {
    const response = await fetch(process.env.API + '/analysis/toptenfood', requestOptions);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error);
  }
};
