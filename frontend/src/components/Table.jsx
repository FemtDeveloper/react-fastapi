import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";
import moment from "moment";
import LeadModal from "./LeadModal";

const Table = () => {
  const [token] = useContext(UserContext);
  const [leads, setLeads] = useState(null);
  const [errorMesssage, setErrorMesssage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);

  const handleUpdate = async (id) => {
    setId(id);
    setActiveModal(true);
  };

  const handleDelete = async (id) => {
    const requestOptions = {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(
      `http://127.0.0.1:8000/api/leads/${id}`,
      requestOptions
    );
    if (!response.ok) {
      setErrorMesssage("Can not deleate lead");
    } else {
      getLeads();
    }
  };

  const getLeads = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(
      "http://127.0.0.1:8000/api/leads",
      requestOptions
    );
    if (!response.ok) {
      setErrorMesssage("Something went wrong");
      setTimeout(() => {
        setErrorMesssage("");
      }, 4000);
    } else {
      const data = await response.json();
      console.log(data);
      setLeads(data);
      setLoaded(true);
    }
  };
  useEffect(() => {
    getLeads();
  }, []);
  const handleModal = () => {
    setActiveModal(!activeModal);
    getLeads();
    setId(null);
  };
  return (
    <>
      <LeadModal
        active={activeModal}
        handleModal={handleModal}
        token={token}
        id={id}
        setErrorMessage={setErrorMesssage}
      />
      <button
        className="button is-fullwidth mb-6 is-primary"
        onClick={() => setActiveModal(true)}
      >
        Create Lead
      </button>
      <ErrorMessage message={errorMesssage} />
      {loaded && leads ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Company</th>
              <th>Email</th>
              <th>Note</th>
              <th>Last Updated</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.id}>
                <td>{lead.first_name}</td>
                <td>{lead.last_name}</td>
                <td>{lead.company}</td>
                <td>{lead.email}</td>
                <td>{lead.note}</td>
                <td>{moment(lead.date_updated).format("MMMM D/YY h:mm a")}</td>
                <td>
                  <button
                    className="is-info is-light button"
                    onClick={() => handleUpdate(lead.id)}
                  >
                    Update
                  </button>
                </td>
                <td>
                  <button
                    className="is-danger is-light button ml-2"
                    onClick={() => handleDelete(lead.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading...</p>
      )}
    </>
  );
};

export default Table;
