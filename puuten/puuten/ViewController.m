//
//  ViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-25.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "ViewController.h"
#import "LoginViewController.h"
@interface ViewController () <LoginViewControllerDelegate>
@property (assign) BOOL login_or_not;
@end

@implementation ViewController
@synthesize login_or_not;

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier hasPrefix:@"login"]) {
        LoginViewController *login = (LoginViewController *)segue.destinationViewController;
        //login.email = @"email";
        //login.password = @"password";
        login.delegate = self;
    }
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

- (void)loadInternetData {
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *libURL = [NSURL URLWithString:@"/home/event_lib/" relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:libURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        arrayData = json;
        [self dataSourceDidLoad];
    }];
    [request setFailedBlock:^{
        [self dataSourceDidError];
    }];
    
    [request startAsynchronous];
    /*
    // Request
    NSString *URLPath = [NSString stringWithFormat:@"http://imgur.com/gallery.json"];
    NSURL *nsURL = [NSURL URLWithString:URLPath];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:nsURL];
    
    [NSURLConnection sendAsynchronousRequest:request queue:[NSOperationQueue mainQueue] completionHandler:^(NSURLResponse *response, NSData *data, NSError *error) {
        
        NSInteger responseCode = [(NSHTTPURLResponse *)response statusCode];
        
        if (!error && responseCode == 200) {
            id res = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingMutableContainers error:nil];
            if (res && [res isKindOfClass:[NSDictionary class]]) {
                
                [arrayData addObjectsFromArray:[res objectForKey:@"gallery"]];
                //arrayData = [[res objectForKey:@"gallery"] retain];
                //NSLog(@"arr == %@",arrayData);
                [self dataSourceDidLoad];
            } else {
                [self dataSourceDidError];
                
                //NSLog(@"arr dataSourceDidError == %@",arrayData);
            }
        } else {
            [self dataSourceDidError];
            //NSLog(@"dataSourceDidError == %@",arrayData);
        }
    }];
    */
}

- (void)dataSourceDidLoad {
    [waterFlow reloadData];
}

- (void)dataSourceDidError {
    [waterFlow reloadData];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	
}

-(void)loadMore{
    
    [arrayData addObjectsFromArray:arrayData];
    [waterFlow reloadData];
}

#pragma mark WaterFlowViewDataSource
- (NSInteger)numberOfColumsInWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return 3;
}

- (NSInteger)numberOfAllWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return [arrayData count];
}

- (UIView *)waterFlowView:(WaterFlowView *)waterFlowView cellForRowAtIndexPath:(IndexPath *)indexPath{
    
    ImageViewCell *view = [[ImageViewCell alloc] initWithIdentifier:nil];
    
    return view;
}


-(void)waterFlowView:(WaterFlowView *)waterFlowView  relayoutCellSubview:(UIView *)view withIndexPath:(IndexPath *)indexPath{
    
    //arrIndex是某个数据在总数组中的索引
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    
    
    NSDictionary *object = [arrayData objectAtIndex:arrIndex];
    
    //NSURL *nsURL = [NSURL URLWithString:[NSString stringWithFormat:@"http://imgur.com/%@%@", [object objectForKey:@"hash"], [object objectForKey:@"ext"]]];
    NSURL *nsURL = [[NSURL alloc] initWithString:[object objectForKey:@"thumbnail_pic"]];
    ImageViewCell *imageViewCell = (ImageViewCell *)view;
    imageViewCell.indexPath = indexPath;
    imageViewCell.columnCount = waterFlowView.columnCount;
    [imageViewCell relayoutViews];
    [(ImageViewCell *)view setImageWithURL:nsURL];
}


#pragma mark WaterFlowViewDelegate
- (CGFloat)waterFlowView:(WaterFlowView *)waterFlowView heightForRowAtIndexPath:(IndexPath *)indexPath{
    /*
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    NSDictionary *dict = [arrayData objectAtIndex:arrIndex];
    
    float width = 0.0f;
    float height = 0.0f;
    if (dict) {
        
        width = [[dict objectForKey:@"width"] floatValue]; 
        height = [[dict objectForKey:@"height"] floatValue];
    }
    
    return waterFlowView.cellWidth * (height/width);
     */
    return waterFlowView.cellWidth*2;
}

- (void)waterFlowView:(WaterFlowView *)waterFlowView didSelectRowAtIndexPath:(IndexPath *)indexPath{
    
    NSLog(@"indexpath row == %d,column == %d",indexPath.row,indexPath.column);
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}
- (void)viewDidAppear:(BOOL)animated
{
    if (!login_or_not) {
        [self performSegueWithIdentifier:@"login" sender:self];
    }
    else {
        arrayData = [[NSMutableArray alloc] init];
        self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"More" style:UIBarButtonItemStyleBordered target:self action:@selector(loadMore)];
        
        waterFlow = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 0, 320, 460-44)];
        waterFlow.waterFlowViewDelegate = self;
        waterFlow.waterFlowViewDatasource = self;
        waterFlow.backgroundColor = [UIColor whiteColor];
        [self.view addSubview:waterFlow];
        //[waterFlow release];
        
        [self loadInternetData];
    }
    [super viewDidAppear:animated];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (void)loginViewController:(LoginViewController *)sender 
               login_or_not:(int)userid
{
    self.login_or_not = YES;
    [self dismissModalViewControllerAnimated:YES];
}

@end
