// window.onload = function () {
//     $(document).ready(function () {
//         fetch(`/userform/dashboard/?user_id=2`)
//             .then((response) => {
//                 console.log('response status: ', response.status);
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then((data) => {
//                 console.log('response data: ', data);
//                 let sidebarData = '';

//                 for (let i = 0; i < data.length; i++) {
//                     sidebarData =
//                         `<li class="active">
//             <a href="#homeSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${data[i].ModuleDescr}</a>
//             <ul class="collapse list-unstyled" id="homeSubmenu">
//                 <li>
//                     <a href="#">Home 1</a>
//                 </li>
//                 <li>
//                     <a href="#">Home 2</a>
//                 </li>
//                 <li>
//                     <a href="#">Home 3</a>
//                 </li>
//             </ul>
//         </li>
//         <li>
//             <a href="#">About</a>
//         </li>
//         <li>
//             <a href="#pageSubmenu" data-toggle="collapse" aria-expanded="false"
//                 class="dropdown-toggle">Pages</a>
//             <ul class="collapse list-unstyled" id="pageSubmenu">
//                 <li>
//                     <a href="#">Page 1</a>
//                 </li>
//                 <li>
//                     <a href="#">Page 2</a>
//                 </li>
//                 <li>
//                     <a href="#">Page 3</a>
//                 </li>
//             </ul>
//         </li>
//         <li>
//             <a href="#">Portfolio</a>
//         </li>
//         <li>
//             <a href="#">Contact</a>
//         </li>`;
//                 }

//                 document.getElementById("sidebarMenu").innerHTML = sidebarData;
//                 // Handle the response data here
//             })
//             .catch((error) => {
//                 console.error('Error:', error);
//                 // Handle errors here
//             });
//     });
// };

// window.onload = function () {
//     $(document).ready(function () {
//         fetch(`/userform/dashboard/?user_id=2`)
//             .then((response) => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then((data) => {
//                 // Group data by ModuleDescr, MnuDescr, and MnuSubDescr
//                 const groupedData = {};
//                 data.forEach(item => {
//                     if (!groupedData[item.ModuleDescr]) {
//                         groupedData[item.ModuleDescr] = {};
//                     }
//                     if (!groupedData[item.ModuleDescr][item.MnuDescr]) {
//                         groupedData[item.ModuleDescr][item.MnuDescr] = {};
//                     }
//                     if (!groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr]) {
//                         groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr] = [];
//                     }
//                     groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr].push(item.FormDescr);
//                 });

//                 // Generate sidebar HTML
//                 let sidebarData = '';
//                 for (const module in groupedData) {
//                     sidebarData += `<li class="active">
//                                         <a href="#${module.replace(/\s+/g, '-').toLowerCase()}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${module}</a>
//                                         <ul class="collapse list-unstyled" id="${module.replace(/\s+/g, '-').toLowerCase()}Submenu">`;
//                     for (const menu in groupedData[module]) {
//                         sidebarData += `<li>
//                                             <a href="#${menu.replace(/\s+/g, '-').toLowerCase()}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${menu}</a>
//                                             <ul class="collapse list-unstyled" id="${menu.replace(/\s+/g, '-').toLowerCase()}Submenu">`;
//                         for (const submenu in groupedData[module][menu]) {
//                             sidebarData += `<li>
//                                                 <a href="#${submenu.replace(/\s+/g, '-').toLowerCase()}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${submenu}</a>
//                                                 <ul class="collapse list-unstyled" id="${submenu.replace(/\s+/g, '-').toLowerCase()}Submenu">`;
//                             groupedData[module][menu][submenu].forEach(form => {
//                                 sidebarData += `<li><a href="#">${form}</a></li>`;
//                             });
//                             sidebarData += `</ul></li>`;
//                         }
//                         sidebarData += `</ul></li>`;
//                     }
//                     sidebarData += `</ul></li>`;
//                 }
//                 document.getElementById("sidebarMenu").innerHTML = sidebarData;
//             })
//             .catch((error) => {
//                 console.error('Error:', error);
//                 // Handle errors here
//             });
//     });
// };


// window.onload = function () {
//     $(document).ready(function () {
//         fetch(`/userform/dashboard/?user_id=2`)
//             .then((response) => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then((data) => {
//                 // Group data by ModuleDescr, MnuDescr, and MnuSubDescr
//                 const groupedData = {};
//                 data.forEach(item => {
//                     if (!groupedData[item.ModuleDescr]) {
//                         groupedData[item.ModuleDescr] = {};
//                     }
//                     if (!groupedData[item.ModuleDescr][item.MnuDescr]) {
//                         groupedData[item.ModuleDescr][item.MnuDescr] = {};
//                     }
//                     if (!groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr]) {
//                         groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr] = [];
//                     }
//                     groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr].push(item.FormDescr);
//                 });

//                 // Generate sidebar HTML
//                 let sidebarData = '';
//                 for (const module in groupedData) {
//                     const moduleID = module.replace(/\s+/g, '-').toLowerCase();
//                     sidebarData += `<li class="active">
//                                         <a href="#${moduleID}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${module}</a>
//                                         <ul class="collapse list-unstyled" id="${moduleID}Submenu">`;
//                     for (const menu in groupedData[module]) {
//                         const menuID = menu.replace(/\s+/g, '-').toLowerCase();
//                         sidebarData += `<li>
//                                             <a href="#${menuID}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${menu}</a>
//                                             <ul class="collapse list-unstyled" id="${menuID}Submenu">`;
//                         for (const submenu in groupedData[module][menu]) {
//                             const submenuID = submenu.replace(/\s+/g, '-').toLowerCase();
//                             sidebarData += `<li>
//                                                 <a href="#${submenuID}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${submenu}</a>
//                                                 <ul class="collapse list-unstyled" id="${submenuID}Submenu">`;
//                             groupedData[module][menu][submenu].forEach(form => {
//                                 sidebarData += `<li><a href="#">${form}</a></li>`;
//                             });
//                             sidebarData += `</ul></li>`;
//                         }
//                         sidebarData += `</ul></li>`;
//                     }
//                     sidebarData += `</ul></li>`;
//                 }
//                 document.getElementById("sidebarMenu").innerHTML = sidebarData;

//                 // Smooth toggling of sub-navbar using jQuery
//                 $('.dropdown-toggle').click(function(e) {
//                     e.preventDefault();
//                     const submenu = $(this).next('.collapse');
//                     submenu.slideToggle();
//                 });
//             })
//             .catch((error) => {
//                 console.error('Error:', error);
//                 // Handle errors here    
//             });
//     });
// };

function onClickFunc(formID, formDescr) {
    console.log('onClickFunc: ', formID, formDescr)
    const message = 'formID: ' + formID + '\n' + 'formDescr: ' + formDescr;
    // alert(message);
    if (formID === 5) {
        window.open('/designation/')
    } else if (formID === 6) {
        window.open('/department/')
    } else if (formID === 4) {
        window.open('/city/')
    } else if (formID === 3) {
        window.open('/employee/')
    } else if (formID === 11) {
        window.open('/grade/')
    } else if (formID === 10) {
        window.open('/loan/');
    } else if (formID === 9) {
        window.open('/leaves/')
    } else if (formID === 7) {
        window.open('/payroll_period/')
    } else if (formID === 8) {
        window.open('/payroll_element/')
    } else if (formID === 12) {
        window.open('/salaryupdate/')
    } else if (formID === 13) {
        window.open('/wda/')
    } else if (formID === 15) {
        window.open('/monthly_all_ded/')
    } else if (formID === 17) {
        window.open('/region/')
    }
}

window.onload = function () {
    $(document).ready(function () {
        alert('shehery')
        const Profile_ID = localStorage.getItem('Profile_ID')
        // const User_ID = localStorage.getItem('User_ID')
        const BASE_URL = window.location.origin;
        fetch(`${BASE_URL}/dashboard/userform/?Profile_ID=${Profile_ID}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                // Group data by ModuleDescr, MnuDescr, and MnuSubDescr
                const groupedData = {};
                console.log('data data: ', data)
                data.forEach(item => {
                    if (!groupedData[item.ModuleDescr]) {
                        groupedData[item.ModuleDescr] = {};
                    }
                    if (!groupedData[item.ModuleDescr][item.MnuDescr]) {
                        groupedData[item.ModuleDescr][item.MnuDescr] = {};
                    }
                    if (!groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr]) {
                        groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr] = new Set(); // Use a Set to store unique form descriptions
                    }
                    if (!groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr].has(item.FormDescr)) {
                        groupedData[item.ModuleDescr][item.MnuDescr][item.MnuSubDescr].add({ formID: item.FormID, formDescr: item.FormDescr }); // Add unique form descriptions to the Set
                    }
                });

                // Generate sidebar HTML
                let sidebarData = '';
                for (const module in groupedData) {
                    const moduleID = module.replace(/\s+/g, '-').toLowerCase();
                    sidebarData += `<li class="active">
                                        <a href="#${moduleID}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${module}</a>
                                        <ul class="collapse list-unstyled" id="${moduleID}Submenu">`;
                    for (const menu in groupedData[module]) {
                        const menuID = menu.replace(/\s+/g, '-').toLowerCase();
                        sidebarData += `<li>
                                            <a href="#${menuID}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${menu}</a>
                                            <ul class="collapse list-unstyled" id="${menuID}Submenu">`;
                        for (const submenu in groupedData[module][menu]) {
                            const submenuID = submenu.replace(/\s+/g, '-').toLowerCase();
                            sidebarData += `<li>
                                                <a href="#${submenuID}Submenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">${submenu}</a>
                                                <ul class="collapse list-unstyled" id="${submenuID}Submenu">`;
                            groupedData[module][menu][submenu].forEach(formDescrObj => {
                                //console.log('formDescrObj: ', formDescrObj)
                                sidebarData += `<li><a onclick="onClickFunc(${formDescrObj.formID}, '${formDescrObj.formDescr}')">${formDescrObj.formDescr}</a></li>`; // Call onClickFunc function on click
                            });
                            sidebarData += `</ul></li>`;
                        }
                        sidebarData += `</ul></li>`;
                    }
                    sidebarData += `</ul></li>`;
                }
                document.getElementById("sidebarMenu").innerHTML = sidebarData;

                // Smooth toggling of sub-navbar using jQuery
                $('.dropdown-toggle').click(function (e) {
                    e.preventDefault();
                    const submenu = $(this).next('.collapse');
                    submenu.slideToggle();
                });
            })
            .catch((error) => {
                console.error('Error:', error);
                // Handle errors here
            });
    });
};


