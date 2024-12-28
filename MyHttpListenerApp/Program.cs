using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;

public class PayrollDetail
{
    public int? EmployeeID { get; set; }
    public string? EmployeeName { get; set; }
    public decimal Salary { get; set; }
    // Add more properties as per the result set returned by your stored procedure
}

class Program
{
    static string connString = "Data Source=192.168.20.166;Initial Catalog=ATS_HRMS_TEST;User ID=tech;Password=tech;Integrated Security=false;";


    static void Main(string[] args)
    {
        HttpListener listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:5000/");
        listener.Start();
        Console.WriteLine("Listening...");

        while (true)
        {
            HttpListenerContext context = listener.GetContext();
            HttpListenerRequest request = context.Request;
            HttpListenerResponse response = context.Response;

            string responseString = string.Empty;

            try
            {
                switch (request.HttpMethod)
                {
                    case "GET":
                        if (request.RawUrl.StartsWith("/ExecuteMonthlyPaySheet"))
                        {
                            responseString = ExecuteMonthlyPaySheet(request);
                        }
                        else if (request.RawUrl.StartsWith("/ExecuteSalaryProcess"))
                        {
                            responseString = ExecuteSalaryProcess(request);
                        }
                        else
                        {
                            responseString = HandleGetRequest(request);
                        }
                        break;
                    case "POST":
                        if (request.RawUrl.StartsWith("/ExecuteSalaryProcess"))
                        {
                            responseString = ExecuteSalaryProcess(request);
                        }
                        else
                        {
                            response.StatusCode = (int)HttpStatusCode.NotFound;
                            responseString = "Not Found";
                        }
                        break;
                    default:
                        response.StatusCode = (int)HttpStatusCode.MethodNotAllowed;
                        responseString = "Method Not Allowed";
                        break;
                }
            }
            catch (Exception ex)
            {
                response.StatusCode = (int)HttpStatusCode.InternalServerError;
                responseString = $"Error: {ex.Message}";
            }

            byte[] buffer = Encoding.UTF8.GetBytes(responseString);
            response.ContentLength64 = buffer.Length;
            Stream output = response.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();
        }
    }

    static string ExecuteMonthlyPaySheet2(HttpListenerRequest request)
    {
        var segments = request.RawUrl.Split('/');
        if (segments.Length == 3 && int.TryParse(segments[2], out int payrollId))
        {
            using (SqlConnection conn = new SqlConnection(connString))
            {
                conn.Open();
                using (SqlCommand cmd = new SqlCommand("HR_Monthly_Pay_Sheet_SP", conn))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("@m_Payroll_ID", payrollId);

                    try
                    {
                        cmd.ExecuteNonQuery(); // Execute the stored procedure
                        return JsonSerializer.Serialize(new
                        {
                            ResponseCode = 200,
                            Message = "Procedure executed successfully",
                            Data = (object)null
                        });
                    }
                    catch (Exception ex)
                    {
                        // Log the exception if needed
                        return JsonSerializer.Serialize(new
                        {
                            ResponseCode = 400,
                            Message = $"Error executing procedure: {ex.Message}",
                            Data = (object)null
                        });
                    }
                }
            }
        }
        else
        {
            return JsonSerializer.Serialize(new
            {
                ResponseCode = 400,
                Message = "Invalid parameters ID",
                Data = (object)null
            });
        }
    }


    static string ExecuteMonthlyPaySheet(HttpListenerRequest request)
    {
        try
        {
            using (var reader = new StreamReader(request.InputStream, request.ContentEncoding))
            {
                string json = reader.ReadToEnd();
                var parameters = JsonSerializer.Deserialize<Dictionary<string, object>>(json);

                if (parameters != null &&
                    parameters.ContainsKey("m_Payroll_ID") && int.TryParse(parameters["m_Payroll_ID"].ToString(), out int payrollId))
                {
                    using (SqlConnection conn = new SqlConnection(connString))
                    {
                        conn.Open();
                        using (SqlCommand cmd = new SqlCommand("HR_Monthly_Pay_Sheet_SP", conn))
                        {
                            cmd.CommandType = CommandType.StoredProcedure;
                            cmd.Parameters.AddWithValue("@m_Payroll_ID", payrollId);

                            cmd.ExecuteNonQuery();
                        }
                    }
                    return JsonSerializer.Serialize(new
                    {
                        ResponseCode = 200,
                        Message = "Procedure executed successfully",
                        Data = (object)null
                    });
                }
                else
                {
                    return JsonSerializer.Serialize(new
                    {
                        ResponseCode = 400,
                        Message = "Invalid parameters",
                        Data = (object)null
                    });
                }
            }
        }
        catch (Exception ex)
        {
            return JsonSerializer.Serialize(new
            {
                ResponseCode = 500,
                Message = $"Error executing procedure: {ex.Message}",
                Data = (object)null
            });
        }
    }


    static string ExecuteSalaryProcess(HttpListenerRequest request)
    {
        try
        {
            using (var reader = new StreamReader(request.InputStream, request.ContentEncoding))
            {
                string json = reader.ReadToEnd();
                var parameters = JsonSerializer.Deserialize<Dictionary<string, object>>(json);

                if (parameters != null &&
                    parameters.ContainsKey("m_Payroll_ID") && int.TryParse(parameters["m_Payroll_ID"].ToString(), out int payrollId) &&
                    parameters.ContainsKey("m_Fuel_Rate") && decimal.TryParse(parameters["m_Fuel_Rate"].ToString(), out decimal fuelRate))
                {
                    using (SqlConnection conn = new SqlConnection(connString))
                    {
                        conn.Open();
                        using (SqlCommand cmd = new SqlCommand("HR_Monthly_Salary_Process", conn))
                        {
                            cmd.CommandType = CommandType.StoredProcedure;
                            cmd.Parameters.AddWithValue("@m_Payroll_ID", payrollId);
                            cmd.Parameters.AddWithValue("@m_Fuel_Rate", fuelRate);

                            cmd.ExecuteNonQuery();
                        }
                    }
                    return JsonSerializer.Serialize(new
                    {
                        ResponseCode = 200,
                        Message = "Procedure executed successfully",
                        Data = (object)null
                    });
                }
                else
                {
                    return JsonSerializer.Serialize(new
                    {
                        ResponseCode = 400,
                        Message = "Invalid parameters",
                        Data = (object)null
                    });
                }
            }
        }
        catch (Exception ex)
        {
            return JsonSerializer.Serialize(new
            {
                ResponseCode = 500,
                Message = $"Error executing procedure: {ex.Message}",
                Data = (object)null
            });
        }
    }


    static string HandleGetRequest(HttpListenerRequest request)
    {
        // Handle other GET requests here
        return "Default GET response";
    }
}
